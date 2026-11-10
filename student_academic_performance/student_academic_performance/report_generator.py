"""
PDF and CSV Report Generator for Student Academic Performance System
Uses ReportLab to generate clean, professional academic performance report PDFs.
"""

import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def generate_student_pdf(student_data, ml_metrics):
    """
    Generates a professional academic performance report PDF for an individual student.
    Returns bytes in a BytesIO buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor('#1e40af')
    dark_text = colors.HexColor('#1e293b')
    light_bg = colors.HexColor('#f8fafc')
    accent_color = colors.HexColor('#3b82f6')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1  # Center
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_text
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=dark_text
    )

    story = []

    # Header
    story.append(Paragraph("STUDENT ACADEMIC PERFORMANCE & PREDICTION SYSTEM", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Official Confidential Performance Evaluation & Improvement Advisory", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=12))

    # Student Identification Card Table
    student_info_data = [
        [
            Paragraph("<b>Student ID:</b>", body_style), Paragraph(str(student_data.get('student_id', 'N/A')), body_style),
            Paragraph("<b>Full Name:</b>", body_style), Paragraph(str(student_data.get('name', 'N/A')), body_style)
        ],
        [
            Paragraph("<b>Department:</b>", body_style), Paragraph(str(student_data.get('department', 'N/A')), body_style),
            Paragraph("<b>Year of Study:</b>", body_style), Paragraph(str(student_data.get('year', 'N/A')), body_style)
        ],
        [
            Paragraph("<b>Email:</b>", body_style), Paragraph(str(student_data.get('email', 'N/A')), body_style),
            Paragraph("<b>Contact:</b>", body_style), Paragraph(str(student_data.get('phone', 'N/A')), body_style)
        ]
    ]

    info_table = Table(student_info_data, colWidths=[100, 160, 100, 170])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 14))

    # Academic & Attendance Metrics Table
    story.append(Paragraph("Academic Activities & Attendance Records", section_heading))
    att = student_data.get('attendance') or {}
    acad = student_data.get('academic_record') or {}

    att_pct = f"{att.get('attendance_percentage', 0.0)}%" if att else "N/A"
    att_days = f"{att.get('days_attended', 0)} / {att.get('total_working_days', 0)} days" if att else "N/A"
    study_hrs = f"{acad.get('study_hours', 0.0)} hrs/day" if acad else "N/A"
    assign_marks = f"{acad.get('assignment_marks', 0.0)} / 100" if acad else "N/A"
    internal_marks = f"{acad.get('internal_marks', 0.0)} / 100" if acad else "N/A"
    prev_sem = f"{acad.get('previous_semester_marks', 0.0)} / 100" if acad else "N/A"
    actual_final = f"{acad.get('actual_final_marks', 'Pending')} / 100" if (acad and acad.get('actual_final_marks') is not None) else "Not Yet Entered"

    metric_data = [
        [Paragraph("<b>Metric Feature</b>", bold_body), Paragraph("<b>Recorded Value</b>", bold_body), Paragraph("<b>Benchmark / Target</b>", bold_body), Paragraph("<b>Status</b>", bold_body)],
        [Paragraph("Attendance Rate", body_style), Paragraph(f"{att_pct} ({att_days})", body_style), Paragraph(">= 75.0%", body_style), Paragraph("Eligible" if (att and att.get('attendance_percentage', 0) >= 75) else "Warning", body_style)],
        [Paragraph("Daily Study Time", body_style), Paragraph(study_hrs, body_style), Paragraph(">= 3.0 hrs/day", body_style), Paragraph("Adequate" if (acad and acad.get('study_hours', 0) >= 3) else "Attention", body_style)],
        [Paragraph("Assignment Marks", body_style), Paragraph(assign_marks, body_style), Paragraph(">= 75.0 / 100", body_style), Paragraph("Good" if (acad and acad.get('assignment_marks', 0) >= 75) else "Moderate", body_style)],
        [Paragraph("Internal Assessment", body_style), Paragraph(internal_marks, body_style), Paragraph(">= 75.0 / 100", body_style), Paragraph("Good" if (acad and acad.get('internal_marks', 0) >= 75) else "Needs Attention", body_style)],
        [Paragraph("Previous Semester", body_style), Paragraph(prev_sem, body_style), Paragraph(">= 60.0 / 100", body_style), Paragraph("Satisfactory" if (acad and acad.get('previous_semester_marks', 0) >= 60) else "Prerequisite Alert", body_style)],
        [Paragraph("Actual Final Marks", bold_body), Paragraph(actual_final, bold_body), Paragraph("Final Exam Record", body_style), Paragraph("Official Record", body_style)]
    ]

    metric_table = Table(metric_data, colWidths=[150, 140, 120, 120])
    metric_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(metric_table)
    story.append(Spacer(1, 14))

    # Machine Learning Prediction Results
    story.append(Paragraph("Machine Learning Prediction Evaluation", section_heading))
    pred = student_data.get('prediction') or {}
    pred_marks = f"{pred.get('predicted_marks', 'N/A')}"
    pred_cat = f"{pred.get('performance_category', 'N/A')}"

    pred_summary_data = [
        [
            Paragraph("<b>Predicted Final Exam Marks:</b>", body_style),
            Paragraph(f"<font size=13 color='#1e40af'><b>{pred_marks} / 100</b></font>", body_style),
            Paragraph("<b>Performance Category:</b>", body_style),
            Paragraph(f"<font size=12 color='#0284c7'><b>{pred_cat}</b></font>", body_style)
        ],
        [
            Paragraph("<b>Algorithm Applied:</b>", body_style),
            Paragraph("Multiple Linear Regression (Scikit-learn)", body_style),
            Paragraph("<b>Model R² Accuracy:</b>", body_style),
            Paragraph(f"{ml_metrics.get('r2_percentage', 86.0)}% (MAE: {ml_metrics.get('mae', 3.17)})", body_style)
        ]
    ]

    pred_table = Table(pred_summary_data, colWidths=[160, 120, 130, 120])
    pred_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1, accent_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bfdbfe')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(pred_table)
    story.append(Spacer(1, 14))

    # Personalized Recommendations & Action Plan
    story.append(Paragraph("Personalized Academic Recommendations & Remedial Plan", section_heading))
    recs = student_data.get('recommendations_data', {})
    summary_text = recs.get('summary', 'Maintain disciplined study habits and regular attendance.')
    story.append(Paragraph(f"<b>Diagnosis:</b> {summary_text}", body_style))
    story.append(Spacer(1, 6))

    action_items = recs.get('action_plan', [
        "Maintain consistent lecture attendance above 85%.",
        "Formulate a structured revision timetable for mid-terms."
    ])
    for idx, item in enumerate(action_items, 1):
        story.append(Paragraph(f"• <b>Action {idx}:</b> {item}", body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#cbd5e1'), spaceAfter=8))
    footer_text = "System Generated Academic Report | Machine Learning Prediction & Improvement Support System | Powered by Scikit-learn & Flask"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=subtitle_style, fontSize=7, textColor=colors.HexColor('#94a3b8'))))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_class_csv(students_list):
    """
    Generates CSV export of all students with their attendance, academic metrics,
    predictions, and actual marks.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        'Student ID',
        'Student Name',
        'Department',
        'Year',
        'Email',
        'Phone',
        'Attendance %',
        'Days Attended',
        'Total Working Days',
        'Daily Study Hours',
        'Assignment Marks',
        'Internal Marks',
        'Previous Semester Marks',
        'Predicted Final Marks',
        'Performance Category',
        'Actual Final Marks'
    ])

    for s in students_list:
        att = s.latest_attendance
        acad = s.latest_academic
        pred = s.latest_prediction

        writer.writerow([
            s.student_id,
            s.name,
            s.department,
            s.year,
            s.email,
            s.phone,
            att.attendance_percentage if att else '',
            att.days_attended if att else '',
            att.total_working_days if att else '',
            acad.study_hours if acad else '',
            acad.assignment_marks if acad else '',
            acad.internal_marks if acad else '',
            acad.previous_semester_marks if acad else '',
            pred.predicted_marks if pred else '',
            pred.performance_category if pred else '',
            acad.actual_final_marks if (acad and acad.actual_final_marks is not None) else ''
        ])

    return output.getvalue()
