import io
import datetime
import pytz

from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from checker.entities import SanctionedEntity
from checker.updater import read_download_timestamps

STANDARD_SPACER_HEIGHT = 12

def to_gmt_string(naive_dt):
    gmt = pytz.timezone('GMT')
    return gmt.localize(naive_dt).strftime('%Y-%m-%d %H:%M:%S %Z')

def generate_sanctions_report(request) -> io.BytesIO:
    """Generate report for Sanctions"""

    # Collect the result information from request body
    body = request.data
    results = body.get('results', {})
    query = ' | '.join([f'"{key}"' for key in results.keys()])
    query_timestamp = body.get('timestamp', '')
    fuzzy = body.get('fuzzy', False)
    threshold = body.get('threshold', 'Unknown')

    doc_stream = io.BytesIO()
    doc = SimpleDocTemplate(
        doc_stream,
        pagesize=portrait(A4),
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = styles['Heading1']
    title_style.alignment = 1
    story.append(Paragraph('Sanctions Report', title_style))

    # Query information
    story.append(Paragraph(f'Query: {query}', styles['Normal']))
    date = to_gmt_string(datetime.datetime.fromtimestamp(float(query_timestamp / 1000))) if query_timestamp else 'Error'
    story.append(Paragraph(f'Date: {date}', styles['Normal']))
    story.append(Paragraph(f'User: {request.user.username}', styles['Normal']))

    timestamp = read_download_timestamps()
    text = ' | '.join([
        f'{authority.upper()} list updated on {to_gmt_string(naive_datetime)}' 
        for authority, naive_datetime in timestamp.items()
        if naive_datetime
    ])

    story.append(Paragraph(text, styles['Normal']))
    if fuzzy: story.append(Paragraph(f'Fuzzy enabled at threshold {threshold}', styles['Normal']))
    story.append(Spacer(1, STANDARD_SPACER_HEIGHT))

    styles.add(ParagraphStyle(
        name='GreenSubtitle', 
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.green
    ))
    styles.add(ParagraphStyle(
        name='OtherSubtitle', 
        fontName='Helvetica-Bold',
        fontSize=14,
    ))

    # Iterate results dict, creating table of results for each key (search term)
    for search_term, results in results.items():
        if len(results) == 0:            
            story.append(Paragraph(f'{search_term} : No results found.', styles['GreenSubtitle']))
        else:
            story.append(Paragraph(f'{search_term} : {len(results)} result{"s" if len(results) > 1 else ""} found.', styles['OtherSubtitle']))

            story.append(Spacer(1, STANDARD_SPACER_HEIGHT))

            # Table of results
            header_style = styles['Normal']
            header_style.textColor = colors.whitesmoke
            table_header = SanctionedEntity.COLUMN_TITLES
            table_header = [Paragraph(title, header_style) for title in table_header]
            table_rows = list(
                [Paragraph(cell) for cell in SanctionedEntity.deserialize(result).row_repr()]
                for result in results
            )
            table_data = [table_header] + table_rows
            table = Table(
                table_data,
            )
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)

            story.append(Spacer(1, STANDARD_SPACER_HEIGHT))
            story.append(table)
        story.append(Spacer(1, STANDARD_SPACER_HEIGHT))
    

    doc.build(story)
    doc_stream.seek(0)
    return doc_stream
