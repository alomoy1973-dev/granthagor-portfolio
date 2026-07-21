from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = "IC_Engine_Exam_Answers_2022_Detailed.pdf"


def p(text, style):
    return Paragraph(text, style)


def bullets(story, items, style):
    for item in items:
        story.append(Paragraph(item, style, bulletText="-"))


def q(story, text, styles):
    story.append(Paragraph(text, styles["Question"]))


def box(lines, style):
    return KeepTogether([Preformatted("\n".join(lines), style), Spacer(1, 4)])


def table(rows, widths):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.3),
        ("LEADING", (0, 0), (-1, -1), 10.4),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#94a3b8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4, leftMargin=1.45 * cm, rightMargin=1.45 * cm,
        topMargin=1.35 * cm, bottomMargin=1.35 * cm,
    )
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="TitleCenter", parent=s["Title"], alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=16.2, leading=20, textColor=colors.HexColor("#172554"), spaceAfter=5))
    s.add(ParagraphStyle(name="SubCenter", parent=s["Normal"], alignment=TA_CENTER, fontSize=9.2, leading=11.7, textColor=colors.HexColor("#374151"), spaceAfter=13))
    s.add(ParagraphStyle(name="Part", parent=s["Heading1"], alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=13.2, leading=16, textColor=colors.white, backColor=colors.HexColor("#1d4ed8"), borderPadding=(5, 4, 5, 4), spaceBefore=8, spaceAfter=9))
    s.add(ParagraphStyle(name="Question", parent=s["Heading2"], fontName="Helvetica-Bold", fontSize=10.55, leading=13.4, textColor=colors.HexColor("#111827"), spaceBefore=9, spaceAfter=4, keepWithNext=True))
    s.add(ParagraphStyle(name="Body", parent=s["BodyText"], fontName="Helvetica", fontSize=9.25, leading=12.2, spaceAfter=4.2))
    s.add(ParagraphStyle(name="ExamBullet", parent=s["BodyText"], leftIndent=14, firstLineIndent=0, bulletIndent=5, fontName="Helvetica", fontSize=9.05, leading=11.8, spaceAfter=2.5))
    s.add(ParagraphStyle(name="SubHead", parent=s["Heading3"], fontName="Helvetica-Bold", fontSize=9.65, leading=12, textColor=colors.HexColor("#1f2937"), spaceBefore=5, spaceAfter=3))
    code = ParagraphStyle("MathBox", parent=s["Code"], fontName="Courier", fontSize=8.2, leading=10.5, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=5, borderWidth=0.45, borderColor=colors.HexColor("#bfdbfe"), borderPadding=6, backColor=colors.HexColor("#f8fbff"))

    story = []
    story.append(p("Internal Combustion Engine: Detailed Exam Answers", s["TitleCenter"]))
    story.append(p("Course: MEE 401 | B.Sc. Mechanical Engineering Examination 2022 question page", s["SubCenter"]))
    story.append(p("PART-A", s["Part"]))

    q(story, "1(a) With proper sketch briefly discuss different components of a typical internal combustion engine.", s)
    story.append(p("A typical reciprocating IC engine consists of fixed parts, moving parts, valve mechanism, fuel system, ignition or injection system, cooling system and lubrication system. These parts work together to convert the chemical energy of fuel into mechanical work at the crankshaft.", s["Body"]))
    story.append(box([
        "Simplified sketch:",
        "",
        "          Spark plug / Injector",
        "                 |",
        "        _________|_________",
        "       |  inlet & exhaust  |  Cylinder head",
        "       |      valves       |",
        "       |-------------------|",
        "       |      Piston       |  Cylinder block",
        "       |___________________|",
        "              |",
        "        Connecting rod",
        "              |",
        "        Crankshaft ---- Flywheel",
        "          Crankcase and oil sump",
    ], code))
    bullets(story, [
        "<b>Cylinder block:</b> Main body of the engine containing cylinder, water jackets and crankcase support.",
        "<b>Cylinder head:</b> Closes the cylinder and carries valves, spark plug or injector.",
        "<b>Piston:</b> Receives gas pressure and transmits force to connecting rod.",
        "<b>Piston rings:</b> Seal the combustion chamber and control lubricating oil.",
        "<b>Connecting rod:</b> Connects piston with crankshaft and transmits force.",
        "<b>Crankshaft:</b> Converts reciprocating motion into rotary motion.",
        "<b>Valves and camshaft:</b> Control intake and exhaust at proper timing.",
        "<b>Flywheel:</b> Stores energy and smooths speed fluctuation.",
        "<b>Crankcase and sump:</b> Enclose crankshaft and store lubricating oil.",
        "<b>Fuel, ignition and cooling systems:</b> Supply fuel, start combustion and control engine temperature.",
    ], s["ExamBullet"])

    q(story, "1(b) Describe the working principle of two-stroke SI engine with proper sketch.", s)
    story.append(p("A two-stroke SI engine completes one cycle in two piston strokes, or one crankshaft revolution. In the simple type, ports are opened and closed by piston movement instead of poppet valves.", s["Body"]))
    story.append(box([
        "Two-stroke SI engine:",
        "",
        "              Spark plug",
        "                 |",
        "          _______|_______",
        "         |               |----> Exhaust port",
        "Transfer |    Piston     |",
        " port -->|_______________|",
        "         |   Crankcase   |<---- Inlet from carburetor",
        "         |_______________|",
    ], code))
    bullets(story, [
        "<b>Upward stroke:</b> The piston moves from BDC to TDC and compresses the charge inside the cylinder. At the same time vacuum is produced in the crankcase and fresh mixture enters through the inlet port.",
        "<b>Ignition:</b> Near TDC the spark plug ignites the compressed air-fuel mixture.",
        "<b>Downward stroke:</b> High-pressure burnt gases push the piston down and useful work is obtained. The fresh mixture in the crankcase is compressed.",
        "<b>Exhaust and transfer:</b> Near BDC the exhaust port opens first, then the transfer port opens and fresh charge enters the cylinder.",
        "<b>Scavenging:</b> Incoming fresh charge pushes exhaust gases out, but some fresh charge may escape, reducing efficiency.",
    ], s["ExamBullet"])

    q(story, "2(a) Find out air-standard efficiency of a constant-volume cycle. Prove that higher compression ratio is the most effective way of improving performance.", s)
    story.append(p("The constant-volume cycle is the Otto cycle, used as the ideal cycle for SI engines. It has isentropic compression, constant-volume heat addition, isentropic expansion and constant-volume heat rejection.", s["Body"]))
    story.append(box([
        "Otto cycle:",
        "  1-2: Isentropic compression",
        "  2-3: Constant-volume heat addition",
        "  3-4: Isentropic expansion",
        "  4-1: Constant-volume heat rejection",
        "",
        "Heat supplied,  Qs = cv(T3 - T2)",
        "Heat rejected,  Qr = cv(T4 - T1)",
        "",
        "eta = 1 - Qr/Qs",
        "    = 1 - (T4 - T1)/(T3 - T2)",
        "",
        "For isentropic processes:",
        "  T2/T1 = r^(k-1),   T3/T4 = r^(k-1)",
        "",
        "Therefore:",
        "             1",
        "  eta = 1 - ---------",
        "          r^(k-1)",
    ], code))
    story.append(p("Here r is compression ratio and k is the ratio of specific heats. Since k is almost fixed for air, the efficiency of the Otto cycle mainly depends on compression ratio. When r increases, the term 1/r^(k-1) decreases, so efficiency increases. Higher compression ratio raises the temperature and pressure before combustion and gives greater expansion work. Therefore increasing compression ratio is the most effective way to improve constant-volume cycle performance, although in practical SI engines it is limited by knocking.", s["Body"]))

    q(story, "2(b) A gas engine works on the constant-volume cycle. Determine salient pressures and temperatures, efficiency, work, mean effective pressure and ideal power.", s)
    story.append(table([
        ["Given data", "Value"],
        ["Bore, D", "280 mm = 0.28 m"],
        ["Stroke, L", "300 mm = 0.30 m"],
        ["Clearance volume, Vc", "1300 cm3 = 0.0013 m3"],
        ["p1, T1", "1 bar, 28 deg C = 301 K"],
        ["Maximum temperature, T3", "1550 deg C = 1823 K"],
        ["cv, R", "0.718 kJ/kg K, 0.287 kJ/kg K"],
        ["Working cycles", "45000 per hour"],
    ], [6.3 * cm, 9.5 * cm]))
    story.append(Spacer(1, 5))
    story.append(box([
        "Step 1: Volumes and compression ratio",
        "  Vs = (pi/4)D^2L = (pi/4)(0.28)^2(0.30) = 0.01847 m3",
        "  V1 = Vs + Vc = 0.01847 + 0.00130 = 0.01977 m3",
        "  V2 = Vc = 0.00130 m3",
        "  r = V1/V2 = 0.01977/0.00130 = 15.21",
        "",
        "  cp = cv + R = 0.718 + 0.287 = 1.005 kJ/kg K",
        "  k = cp/cv = 1.005/0.718 = 1.40 approximately",
    ], code))
    story.append(box([
        "Step 2: Compression 1-2",
        "  T2 = T1 r^(k-1) = 301 x 15.21^0.4 = 893 K",
        "  p2 = p1 r^k     = 1 x 15.21^1.4   = 45.15 bar",
        "",
        "Step 3: Constant-volume heat addition 2-3",
        "  p3/T3 = p2/T2",
        "  p3 = 45.15 x (1823/893) = 92.12 bar",
        "",
        "Step 4: Expansion 3-4",
        "  T4 = T3/r^(k-1) = 1823/15.21^0.4 = 614 K",
        "  p4 = p3/r^k     = 92.12/15.21^1.4 = 2.04 bar",
    ], code))
    story.append(box([
        "Step 5: Efficiency, work and power",
        "  eta = 1 - 1/r^(k-1)",
        "      = 1 - 1/15.21^0.4 = 0.663 = 66.3%",
        "",
        "  m = p1V1/(RT1) = (100 x 0.01977)/(0.287 x 301)",
        "    = 0.02289 kg",
        "",
        "  w = cv[(T3 - T2) - (T4 - T1)]",
        "    = 0.718[(1823 - 893) - (614 - 301)]",
        "    = 442.6 kJ/kg",
        "",
        "  Work per cycle = m x w = 0.02289 x 442.6 = 10.13 kJ",
        "  mep = Work/Vs = 10.13/0.01847 = 548 kPa = 5.48 bar",
        "  Power = 10.13 x (45000/3600) = 126.6 kW",
    ], code))
    story.append(table([
        ["Final result", "Answer"],
        ["p2, T2", "45.15 bar, 893 K"],
        ["p3, T3", "92.12 bar, 1823 K"],
        ["p4, T4", "2.04 bar, 614 K"],
        ["Air-standard efficiency", "66.3%"],
        ["Work per cycle", "10.13 kJ"],
        ["Mean effective pressure", "5.48 bar"],
        ["Ideal power", "126.6 kW"],
    ], [6.3 * cm, 9.5 * cm]))

    q(story, "3(a) Draw P-V and T-S diagram for Otto cycle, Diesel cycle and Dual cycle.", s)
    story.append(p("The three air-standard cycles are represented qualitatively below. Vertical lines in a P-V diagram show constant volume, while horizontal-like heat addition in Diesel cycle occurs at constant pressure. In T-S diagrams, isentropic processes are vertical lines.", s["Body"]))
    story.append(box([
        "Otto cycle:",
        "  P-V: 1-2 isentropic compression, 2-3 constant-volume heat addition,",
        "       3-4 isentropic expansion, 4-1 constant-volume heat rejection.",
        "  T-S: 1-2 and 3-4 vertical isentropic lines; 2-3 heat addition; 4-1 rejection.",
        "",
        "Diesel cycle:",
        "  P-V: 1-2 isentropic compression, 2-3 constant-pressure heat addition,",
        "       3-4 isentropic expansion, 4-1 constant-volume heat rejection.",
        "  T-S: 1-2 and 3-4 vertical; 2-3 heat addition at constant pressure.",
        "",
        "Dual cycle:",
        "  P-V: 1-2 isentropic compression, 2-3 constant-volume heat addition,",
        "       3-4 constant-pressure heat addition, 4-5 isentropic expansion,",
        "       5-1 constant-volume heat rejection.",
        "  T-S: Combination of Otto and Diesel heat addition processes.",
    ], code))

    q(story, "3(b) Briefly explain refining process of petroleum.", s)
    story.append(p("Petroleum refining converts crude oil into useful fuels and lubricants. Crude petroleum is first cleaned, then separated by boiling range, and finally chemically treated or converted to improve quality.", s["Body"]))
    bullets(story, [
        "<b>Desalting:</b> Water, salts and solid impurities are removed to reduce corrosion and fouling.",
        "<b>Fractional distillation:</b> Heated crude oil enters a fractionating column. Light gases, petrol, naphtha, kerosene, diesel, lubricating oil and residue are separated at different heights according to boiling point.",
        "<b>Cracking:</b> Heavy hydrocarbons are broken into lighter useful fuels by thermal or catalytic cracking.",
        "<b>Reforming:</b> Low-octane hydrocarbons are converted into high-octane petrol components.",
        "<b>Treating:</b> Sulphur, gum and other impurities are removed.",
        "<b>Blending:</b> Fractions and additives are mixed to obtain required fuel properties such as octane number, viscosity and volatility.",
    ], s["ExamBullet"])

    q(story, "4(a) Is it suitable to use Hydrogen Gas as a fuel for IC engine? Briefly explain.", s)
    story.append(p("Hydrogen can be used as a fuel in IC engines, especially SI engines, because it has high flame speed, wide flammability range and clean combustion. Its main combustion product is water vapour, so carbon monoxide, carbon dioxide and unburnt hydrocarbon emissions are very low.", s["Body"]))
    bullets(story, [
        "<b>Advantages:</b> high calorific value per kg, clean exhaust, high flame speed, lean-burn capability and good anti-knock property.",
        "<b>Difficulties:</b> very low density, storage problem, high-pressure or cryogenic tank requirement, possibility of backfire/pre-ignition, leakage risk and production cost.",
        "<b>Suitability:</b> It is technically suitable, but special fuel storage, metering, safety and combustion-control arrangements are needed. Therefore it is promising but not as convenient as petrol or diesel in ordinary engines.",
    ], s["ExamBullet"])

    q(story, "4(b) What is engine knocking? Why engine knocks? What are Octane rating and Cetane rating of fuel?", s)
    story.append(p("Engine knocking is abnormal combustion that produces a sharp metallic sound and rapid pressure oscillation inside the cylinder. It reduces power, increases heat transfer and may damage piston, rings, bearings and cylinder head.", s["Body"]))
    bullets(story, [
        "<b>SI engine knock:</b> The unburnt end gas auto-ignites before the normal flame front reaches it. Causes include high compression ratio, low-octane fuel, high inlet temperature, excessive spark advance, deposits and overheating.",
        "<b>CI engine knock:</b> Long ignition delay allows fuel to accumulate before ignition. When it burns suddenly, pressure rises very rapidly.",
        "<b>Octane rating:</b> Measure of anti-knock quality of SI fuel. Iso-octane is 100 and normal heptane is 0.",
        "<b>Cetane rating:</b> Measure of ignition quality of diesel fuel. Higher cetane number means shorter ignition delay and smoother diesel combustion.",
    ], s["ExamBullet"])

    story.append(PageBreak())
    story.append(p("PART-B", s["Part"]))

    q(story, "1(a) Write down the wet sump lubricant system.", s)
    story.append(p("In a wet sump lubrication system, lubricating oil is stored in the oil sump at the bottom of the crankcase. It is the most common system used in automobile engines because it is simple, compact and economical.", s["Body"]))
    bullets(story, [
        "Oil is stored in the sump and drawn by an oil pump through a strainer.",
        "The pump sends oil under pressure through an oil filter to the main oil gallery.",
        "From the gallery, oil reaches main bearings, big-end bearings, camshaft bearings and valve gear.",
        "Oil splashed from rotating parts lubricates cylinder walls, piston pins and other surfaces.",
        "After lubrication and cooling, oil drains back to the sump by gravity.",
        "A pressure relief valve prevents excessive oil pressure, and a dipstick is used to check oil level.",
    ], s["ExamBullet"])

    q(story, "1(b) What are concentric and eccentric carburetors? Compare battery and magneto ignition system.", s)
    story.append(p("<b>Concentric carburetor:</b> The fuel jet is located approximately at the centre of the venturi throat, giving symmetrical air flow and uniform mixture. <b>Eccentric carburetor:</b> The fuel jet is offset from the centre line, usually for constructional or flow-arrangement reasons.", s["Body"]))
    story.append(table([
        ["Basis", "Battery ignition", "Magneto ignition"],
        ["Source of energy", "Battery supplies current.", "Magneto generates its own current."],
        ["Starting", "Good spark at low speed if battery is charged.", "Weak spark at very low speed."],
        ["Battery need", "Battery required.", "Battery not required during running."],
        ["Maintenance", "Battery charging and care needed.", "Less battery maintenance."],
        ["Application", "Cars and light vehicles.", "Motorcycles, small engines, aircraft."],
        ["Reliability", "Depends on battery condition.", "More self-contained and reliable for remote use."],
    ], [3.5 * cm, 6.2 * cm, 6.2 * cm]))

    q(story, "2(a) Mention some necessity of engine cooling. Explain gas temperature variation curve for a typical four-stroke SI engine.", s)
    bullets(story, [
        "Cooling prevents overheating of cylinder, piston, valves and cylinder head.",
        "It maintains lubricating oil viscosity and prevents oil burning.",
        "It avoids thermal distortion and seizure of piston.",
        "It reduces knocking tendency and protects engine materials.",
        "It maintains proper clearances and improves durability.",
        "It helps the engine operate at a suitable steady temperature.",
    ], s["ExamBullet"])
    story.append(p("During suction, gas temperature is low because fresh mixture enters. During compression, temperature rises. Spark occurs before TDC and combustion raises temperature rapidly, with maximum temperature just after TDC. During expansion, temperature falls as gases do work. During exhaust, hot gases leave and temperature decreases further.", s["Body"]))
    story.append(box([
        "Temperature",
        "   ^                    peak after TDC",
        "   |                       /\\",
        "   |                      /  \\",
        "   |     compression     /    \\ expansion",
        "   |___ suction ________/      \\____ exhaust",
        "   +------------------------------------------> crank angle",
    ], code))

    q(story, "2(b) How can an engine be air cooled? Mention different types of cooling fins.", s)
    story.append(p("In air cooling, heat from the cylinder and head is transferred directly to atmospheric air. Fins are provided on the outside surface to increase heat-transfer area. Air flow may be natural due to vehicle motion or forced by a fan and shroud.", s["Body"]))
    bullets(story, [
        "Heat flows from combustion gases to cylinder wall and head.",
        "The metal conducts heat to the outer fin surfaces.",
        "Air flows over the fins and removes heat by convection.",
        "Air cooling is simple, light and avoids radiator, pump and coolant leakage.",
        "It is common in motorcycles, small engines, aircraft engines and portable engines.",
    ], s["ExamBullet"])
    story.append(p("<b>Types of cooling fins:</b> annular or circumferential fins, longitudinal fins, pin fins, tapered fins, straight fins, interrupted fins and spiral/helical fins. Fin spacing must allow sufficient air flow; very close fins may reduce cooling due to poor air circulation.", s["Body"]))

    q(story, "3(a) Mention difference between supercharger and turbocharger. What are pollutant formations?", s)
    story.append(table([
        ["Basis", "Supercharger", "Turbocharger"],
        ["Drive", "Driven by crankshaft.", "Driven by exhaust gas turbine."],
        ["Energy source", "Consumes engine power.", "Uses exhaust energy."],
        ["Response", "Fast response, little lag.", "May have turbo lag."],
        ["Efficiency", "Boosts power but has mechanical loss.", "Usually improves efficiency."],
        ["Construction", "Mechanical drive needed.", "Turbine and high-temperature parts needed."],
    ], [3.5 * cm, 6.2 * cm, 6.2 * cm]))
    story.append(p("<b>Pollutant formation:</b> IC engines produce pollutants because combustion is not perfectly ideal. Carbon monoxide forms due to incomplete combustion in rich mixtures. Unburnt hydrocarbons arise from flame quenching, crevice volume and misfire. Nitrogen oxides form at high combustion temperature when nitrogen and oxygen combine. Soot or smoke forms in diesel engines due to locally rich fuel zones. Sulphur oxides form when sulphur in fuel burns.", s["Body"]))

    q(story, "3(b) Write down the advantages and disadvantages of two-stroke engines.", s)
    story.append(p("<b>Advantages:</b>", s["Body"]))
    bullets(story, [
        "One power stroke occurs in every crankshaft revolution.",
        "Power-to-weight ratio is high.",
        "Construction is simple and compact.",
        "Initial cost is low because fewer parts are used.",
        "Turning moment is more uniform than a single-cylinder four-stroke engine.",
    ], s["ExamBullet"])
    story.append(p("<b>Disadvantages:</b>", s["Body"]))
    bullets(story, [
        "Fuel consumption is higher due to short-circuiting of fresh charge.",
        "Scavenging is imperfect and thermal efficiency is lower.",
        "Lubrication is more difficult.",
        "Exhaust emissions and smoke are higher.",
        "Engine parts may wear faster due to higher thermal and mechanical loading.",
    ], s["ExamBullet"])

    q(story, "4. Write down short note on the following.", s)
    story.append(p("(a) Scavenging.", s["SubHead"]))
    story.append(p("Scavenging is the process of removing burnt gases from the cylinder and replacing them with fresh charge or air. It is especially important in two-stroke engines because exhaust and charging occur during a short time near BDC. Good scavenging increases power, efficiency and combustion quality.", s["Body"]))
    story.append(p("(b) Piston cooling.", s["SubHead"]))
    story.append(p("The piston receives heat from hot combustion gases. It is cooled by conduction through piston rings to the cylinder wall, by oil splash or oil jet on the underside, and by heat flow through the piston pin and connecting rod. Proper piston cooling prevents seizure, ring sticking and piston crown damage.", s["Body"]))
    story.append(p("(c) Spark plug and fuel injector.", s["SubHead"]))
    story.append(p("A spark plug produces an electric spark in an SI engine to ignite the compressed mixture. A fuel injector supplies fuel in atomized form. In CI engines it injects diesel at high pressure near the end of compression; in modern SI engines injectors may supply petrol into the port or directly into the cylinder.", s["Body"]))
    story.append(p("(d) Condenser.", s["SubHead"]))
    story.append(p("A condenser, or capacitor, is connected across the contact breaker points in a battery ignition system. It prevents heavy sparking at the points and helps the magnetic field in the ignition coil collapse rapidly, producing a high secondary voltage.", s["Body"]))
    story.append(p("(e) Ballast resistor.", s["SubHead"]))
    story.append(p("A ballast resistor is connected in series with the ignition coil primary circuit to limit current during normal running. It prevents overheating of the coil and contact points. During starting it may be bypassed to provide a stronger spark.", s["Body"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(1.45 * cm, 0.78 * cm, "Detailed IC Engine Exam Answers - 2022")
        canvas.drawRightString(A4[0] - 1.45 * cm, 0.78 * cm, f"Page {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUT)
