from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = "ICE_MEE401_Topicwise_Solved.pdf"


def p(text, style):
    return Paragraph(text, style)


def bullets(story, items, style):
    for item in items:
        story.append(Paragraph(item, style, bulletText="-"))


def box(lines, style):
    return KeepTogether([Preformatted("\n".join(lines), style), Spacer(1, 4)])


def tbl(rows, widths):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.0),
        ("LEADING", (0, 0), (-1, -1), 10.0),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#94a3b8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def topic(story, number, title, styles, tag=None):
    label = f"{number}. {title}" if tag is None else f"{number}. {title} ({tag})"
    story.append(Paragraph(label, styles["Topic"]))


def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=1.35 * cm,
        rightMargin=1.35 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.25 * cm,
    )

    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="TitleCenter", parent=s["Title"], alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=16.5, leading=20, textColor=colors.HexColor("#172554"), spaceAfter=5))
    s.add(ParagraphStyle(name="SubCenter", parent=s["Normal"], alignment=TA_CENTER, fontSize=9.2, leading=11.6, textColor=colors.HexColor("#374151"), spaceAfter=12))
    s.add(ParagraphStyle(name="Part", parent=s["Heading1"], alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=13.2, leading=16, textColor=colors.white, backColor=colors.HexColor("#1d4ed8"), borderPadding=(5, 4, 5, 4), spaceBefore=8, spaceAfter=8))
    s.add(ParagraphStyle(name="Topic", parent=s["Heading2"], fontName="Helvetica-Bold", fontSize=10.7, leading=13.5, textColor=colors.HexColor("#111827"), spaceBefore=9, spaceAfter=4, keepWithNext=True))
    s.add(ParagraphStyle(name="SubHead", parent=s["Heading3"], fontName="Helvetica-Bold", fontSize=9.45, leading=11.6, textColor=colors.HexColor("#1f2937"), spaceBefore=5, spaceAfter=3))
    s.add(ParagraphStyle(name="Body", parent=s["BodyText"], fontName="Helvetica", fontSize=8.95, leading=11.8, spaceAfter=4))
    s.add(ParagraphStyle(name="ExamBullet", parent=s["BodyText"], leftIndent=14, firstLineIndent=0, bulletIndent=5, fontName="Helvetica", fontSize=8.75, leading=11.4, spaceAfter=2.2))
    code = ParagraphStyle("MathBox", parent=s["Code"], fontName="Courier", fontSize=7.85, leading=10.0, leftIndent=7, rightIndent=7, spaceBefore=4, spaceAfter=5, borderWidth=0.4, borderColor=colors.HexColor("#bfdbfe"), borderPadding=6, backColor=colors.HexColor("#f8fbff"))

    story = []
    story.append(p("MEE 401 Internal Combustion Engines", s["TitleCenter"]))
    story.append(p("Topic-wise Solved Question Bank from Past Exams (2019, 2021, 2022)", s["SubCenter"]))

    story.append(p("PART A - Theory of Engines, Cycles and Fuels", s["Part"]))

    topic(story, 1, "Engine Classification and Basic Components", s, "Repeated")
    story.append(p("IC engines are classified according to their cycle, fuel, ignition, strokes, cooling, cylinder arrangement and application. A typical engine is a combination of fixed parts, moving parts and auxiliary systems.", s["Body"]))
    bullets(story, [
        "<b>Cycle:</b> Otto, Diesel and Dual-combustion cycle engines.",
        "<b>Ignition:</b> spark ignition (SI) and compression ignition (CI).",
        "<b>Strokes:</b> two-stroke and four-stroke engines.",
        "<b>Fuel:</b> petrol, diesel, gas, alcohol, hydrogen and multi-fuel engines.",
        "<b>Cooling:</b> air-cooled and water-cooled engines.",
        "<b>Cylinder arrangement:</b> vertical, horizontal, in-line, V-type, opposed and radial.",
        "<b>Charging:</b> naturally aspirated, supercharged and turbocharged.",
        "<b>Application:</b> automobile, marine, aircraft, locomotive and stationary engines.",
    ], s["ExamBullet"])
    story.append(box([
        "Typical IC engine components:",
        "",
        "          Spark plug / Injector",
        "                 |",
        "        _________|_________   Cylinder head",
        "       |  inlet & exhaust  |",
        "       |      valves       |",
        "       |-------------------|",
        "       |      Piston       |   Cylinder block",
        "       |___________________|",
        "              |",
        "        Connecting rod",
        "              |",
        "        Crankshaft ---- Flywheel",
        "          Crankcase and oil sump",
    ], code))
    bullets(story, [
        "<b>Cylinder block:</b> contains cylinder and supports main parts. <b>Cylinder head:</b> closes the cylinder and carries valves, plug or injector.",
        "<b>Piston and rings:</b> receive gas pressure, seal combustion chamber and control oil.",
        "<b>Connecting rod and crankshaft:</b> transmit force and convert reciprocating motion to rotary motion.",
        "<b>Camshaft and valve gear:</b> operate inlet and exhaust valves at proper timing.",
        "<b>Flywheel:</b> stores energy and smooths engine speed.",
    ], s["ExamBullet"])

    topic(story, 2, "Air Standard Cycle - Basic Concepts", s)
    story.append(p("An air-standard cycle is an idealized thermodynamic cycle used to analyze IC engines. The real engine process is replaced by a closed cycle using air as the working fluid.", s["Body"]))
    bullets(story, [
        "Air behaves as an ideal gas and circulates in a closed cycle.",
        "Combustion is replaced by external heat addition.",
        "Exhaust is replaced by heat rejection to a sink.",
        "Compression and expansion are assumed reversible adiabatic.",
        "Specific heats are often assumed constant at room temperature.",
        "Pressure losses, friction, heat leakage and gas exchange losses are neglected.",
    ], s["ExamBullet"])
    story.append(p("The ideal cycle has sharp, clean thermodynamic processes. The actual cycle is smaller due to pumping loss, heat loss, incomplete combustion, valve timing effects and friction.", s["Body"]))

    topic(story, 3, "Valve Timing Diagram of Four-Stroke SI Engine", s, "Repeated")
    story.append(p("In an actual four-stroke SI engine, valves open early and close late because gas flow is not instantaneous. Proper valve timing improves volumetric efficiency and reduces pumping loss.", s["Body"]))
    bullets(story, [
        "<b>Inlet valve opens:</b> about 10-20 degrees before TDC near the end of exhaust stroke.",
        "<b>Inlet valve closes:</b> about 30-45 degrees after BDC to use inertia of incoming charge.",
        "<b>Spark advance:</b> about 20-35 degrees before TDC so peak pressure occurs just after TDC.",
        "<b>Exhaust valve opens:</b> about 35-50 degrees before BDC to release pressure before exhaust stroke.",
        "<b>Exhaust valve closes:</b> about 10-15 degrees after TDC. The period when both valves are open is valve overlap.",
    ], s["ExamBullet"])
    story.append(box([
        "Typical SI valve timing:",
        "  IVO = 10-20 deg BTDC      IVC = 30-45 deg ABDC",
        "  EVO = 35-50 deg BBDC      EVC = 10-15 deg ATDC",
        "  Spark = 20-35 deg BTDC",
    ], code))

    topic(story, 4, "Two-Stroke SI Engine - Working Principle", s, "Repeated")
    story.append(p("A two-stroke SI engine completes one cycle in two piston strokes, or one crankshaft revolution. The piston itself opens and closes the inlet, transfer and exhaust ports in the simple type.", s["Body"]))
    story.append(box([
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
        "<b>Upward stroke:</b> charge in the cylinder is compressed; fresh mixture enters crankcase due to vacuum.",
        "<b>Ignition:</b> spark occurs near TDC and combustion raises pressure.",
        "<b>Downward stroke:</b> gases expand and produce power; crankcase charge is compressed.",
        "<b>Exhaust and transfer:</b> exhaust port opens first, then transfer port admits fresh charge.",
        "<b>Scavenging:</b> incoming charge pushes out burnt gases, but some fresh charge may escape.",
    ], s["ExamBullet"])

    topic(story, 5, "Air Standard Efficiency Derivations", s, "Most Important")
    story.append(p("The air-standard efficiency derivations for Otto, Diesel and constant-volume cycles are highly repeated. The constant-volume cycle is the Otto cycle.", s["Body"]))
    story.append(box([
        "Otto / constant-volume cycle:",
        "  Qs = cv(T3 - T2),   Qr = cv(T4 - T1)",
        "  eta = 1 - Qr/Qs",
        "",
        "For isentropic compression and expansion:",
        "  T2/T1 = r^(k-1),   T3/T4 = r^(k-1)",
        "",
        "Therefore:",
        "             1",
        "  eta_o = 1 - ---------",
        "          r^(k-1)",
    ], code))
    story.append(box([
        "Diesel cycle:",
        "  r   = compression ratio = V1/V2",
        "  rho = cut-off ratio = V3/V2",
        "",
        "                 1        (rho^k - 1)",
        "  eta_d = 1 - --------- x ----------------",
        "              r^(k-1)     k(rho - 1)",
    ], code))
    story.append(p("For a given working fluid k is almost constant, so increasing compression ratio is the most effective way to improve Otto-cycle efficiency. In Diesel cycle, efficiency increases with compression ratio but decreases as cut-off ratio increases. Mean effective pressure increases with initial pressure because higher initial pressure means more mass of working fluid in the cylinder, giving more heat release and more work for the same swept volume.", s["Body"]))

    topic(story, 6, "Numerical Problem - Constant Volume Cycle Gas Engine", s, "Repeated")
    story.append(tbl([
        ["Given", "Value"],
        ["Bore and stroke", "D = 0.28 m, L = 0.30 m"],
        ["Clearance volume", "Vc = 1300 cm3 = 0.0013 m3"],
        ["Initial state", "p1 = 1 bar, T1 = 28 deg C = 301 K"],
        ["Maximum temperature", "T3 = 1550 deg C = 1823 K"],
        ["Constants", "cv = 0.718 kJ/kgK, R = 0.287 kJ/kgK"],
        ["Cycles", "45000 cycles/hour"],
    ], [5.1 * cm, 10.6 * cm]))
    story.append(Spacer(1, 4))
    story.append(box([
        "Swept volume:",
        "  Vs = (pi/4)D^2L = (pi/4)(0.28)^2(0.30) = 0.01847 m3",
        "",
        "Total volume:",
        "  V1 = Vs + Vc = 0.01847 + 0.00130 = 0.01977 m3",
        "  V2 = Vc = 0.00130 m3",
        "  r = V1/V2 = 15.21",
        "",
        "k = (cv + R)/cv = (0.718 + 0.287)/0.718 = 1.40",
    ], code))
    story.append(box([
        "Compression 1-2:",
        "  T2 = T1 r^(k-1) = 301 x 15.21^0.4 = 893 K",
        "  p2 = p1 r^k     = 1 x 15.21^1.4   = 45.15 bar",
        "",
        "Constant-volume heat addition 2-3:",
        "  p3 = p2(T3/T2) = 45.15(1823/893) = 92.12 bar",
        "",
        "Expansion 3-4:",
        "  T4 = T3/r^(k-1) = 1823/15.21^0.4 = 614 K",
        "  p4 = p3/r^k     = 92.12/15.21^1.4 = 2.04 bar",
    ], code))
    story.append(box([
        "Efficiency, work, mep and power:",
        "  eta = 1 - 1/r^(k-1) = 1 - 1/15.21^0.4 = 66.3%",
        "",
        "  m = p1V1/(RT1) = (100 x 0.01977)/(0.287 x 301) = 0.02289 kg",
        "",
        "  w = cv[(T3 - T2) - (T4 - T1)]",
        "    = 0.718[(1823 - 893) - (614 - 301)] = 442.6 kJ/kg",
        "",
        "  Work/cycle = 0.02289 x 442.6 = 10.13 kJ",
        "  mep = 10.13/0.01847 = 548 kPa = 5.48 bar",
        "  Power = 10.13 x (45000/3600) = 126.6 kW",
    ], code))

    topic(story, 7, "P-V and T-S Diagrams for Otto, Diesel and Dual Cycles", s, "Repeated")
    story.append(box([
        "Otto cycle:",
        "  P-V: 1-2 isentropic compression, 2-3 constant-volume heat addition,",
        "       3-4 isentropic expansion, 4-1 constant-volume heat rejection.",
        "  T-S: 1-2 and 3-4 vertical isentropic lines.",
        "",
        "Diesel cycle:",
        "  P-V: 1-2 isentropic compression, 2-3 constant-pressure heat addition,",
        "       3-4 isentropic expansion, 4-1 constant-volume heat rejection.",
        "",
        "Dual cycle:",
        "  P-V: 1-2 isentropic compression, 2-3 constant-volume heat addition,",
        "       3-4 constant-pressure heat addition, 4-5 isentropic expansion,",
        "       5-1 constant-volume heat rejection.",
    ], code))

    topic(story, 8, "Engine Knocking, Octane and Cetane Rating", s, "Most Important")
    story.append(p("Knocking is abnormal combustion that causes pressure waves and a sharp metallic sound. It reduces power and may damage engine parts.", s["Body"]))
    bullets(story, [
        "<b>SI knock:</b> unburnt end gas auto-ignites before the normal flame front reaches it. Causes include high compression ratio, low octane fuel, excessive spark advance, high inlet temperature, deposits and overheating.",
        "<b>CI knock:</b> long ignition delay allows too much diesel to accumulate before burning; sudden combustion causes rapid pressure rise.",
        "<b>Octane number:</b> measure of anti-knock quality of SI fuel. Iso-octane = 100, normal heptane = 0.",
        "<b>Cetane number:</b> measure of ignition quality of diesel fuel. Higher cetane number gives shorter ignition delay and smoother combustion.",
    ], s["ExamBullet"])

    topic(story, 9, "IC Engine Fuels - Properties, Refining and Alternative Fuels", s)
    bullets(story, [
        "<b>Requirements of IC fuel:</b> high calorific value, proper volatility, low sulphur, low ash, easy starting, safe storage, low deposits, suitable ignition quality and reasonable cost.",
        "<b>SI fuel properties:</b> high octane number, suitable volatility, low gum, clean burning and good vaporization.",
        "<b>CI fuel properties:</b> high cetane number, proper viscosity, good atomization, high calorific value, low sulphur, low carbon residue and suitable pour point.",
        "<b>LPG:</b> mainly propane and butane stored under moderate pressure; clean SI fuel. <b>LNG:</b> mainly methane stored cryogenically; clean but storage is difficult.",
        "<b>Volatility:</b> important because SI fuel must vaporize and mix with air; too low volatility gives poor starting, too high causes vapour lock.",
    ], s["ExamBullet"])
    story.append(p("<b>Petroleum refining:</b> crude oil is desalted, heated and separated by fractional distillation into gases, petrol, kerosene, diesel, lubricating oil and residue. Heavy fractions may be cracked into lighter fuels, reformed to improve octane number, treated to remove sulphur and blended to meet specifications.", s["Body"]))
    story.append(p("<b>Solid fuels:</b> coal, coke, charcoal and biomass cannot be used directly in normal IC engines because they cannot be atomized or metered quickly, burn slowly and produce ash/deposits. They may first be converted to producer gas. <b>Hydrogen:</b> suitable in principle because it burns cleanly and has high flame speed, but storage, leakage, pre-ignition and cost are major difficulties.", s["Body"]))

    story.append(PageBreak())
    story.append(p("PART B - Components, Systems and Short Notes", s["Part"]))

    topic(story, 10, "Carburetor - Requirements and Working Principle", s, "Repeated")
    bullets(story, [
        "An ideal carburetor should provide correct air-fuel ratio at starting, idling, cruising, acceleration and full load.",
        "It should atomize fuel finely, distribute mixture uniformly, respond quickly and be simple and reliable.",
        "It supplies rich mixture for starting and acceleration, lean mixture for economy and correct mixture for normal running.",
    ], s["ExamBullet"])
    story.append(p("In a simple carburetor, air passes through a venturi. At the throat, velocity rises and pressure falls. Fuel from the float chamber is discharged through the jet into this low-pressure region, atomized by the air stream and sent to the engine. The throttle controls mixture quantity; the choke enriches mixture during cold starting.", s["Body"]))

    topic(story, 11, "Carburetor Types, Choke and Carburetor Icing", s)
    bullets(story, [
        "<b>Choke:</b> a valve placed before the venturi to restrict air flow during cold starting; it enriches the mixture.",
        "<b>Downdraught carburetor:</b> air flows downward; good breathing and common in automobiles.",
        "<b>Updraught carburetor:</b> air flows upward; reduces flooding risk but has higher flow resistance.",
        "<b>Horizontal draught:</b> air flows horizontally; used where height is limited.",
        "<b>Carburetor icing:</b> occurs when fuel vaporization and pressure drop lower air temperature below freezing; moisture freezes near venturi/throttle and restricts flow.",
    ], s["ExamBullet"])

    topic(story, 12, "Concentric/Eccentric Carburetor and Ignition System Comparison", s, "Repeated")
    story.append(p("A concentric carburetor has the fuel jet approximately on the centre line of the venturi, giving symmetrical flow. An eccentric carburetor has the fuel jet offset from the centre line for constructional or flow reasons.", s["Body"]))
    story.append(tbl([
        ["Basis", "Battery ignition", "Magneto ignition"],
        ["Source", "Battery supplies current.", "Magneto generates its own current."],
        ["Low-speed spark", "Good if battery is charged.", "Comparatively weak at very low speed."],
        ["Battery", "Required.", "Not required during running."],
        ["Maintenance", "Battery needs care.", "Self-contained and reliable."],
        ["Use", "Cars and light vehicles.", "Motorcycles, small engines, aircraft."],
    ], [3.3 * cm, 6.2 * cm, 6.2 * cm]))

    topic(story, 13, "Battery Ignition System and Spark Plug", s)
    story.append(p("In a battery ignition system, the battery supplies low-voltage current to the primary winding of the ignition coil. When the contact breaker opens, the primary current is interrupted and a high voltage is induced in the secondary winding. The distributor sends this high voltage to the proper spark plug in firing order.", s["Body"]))
    bullets(story, [
        "<b>Battery:</b> source of electrical energy. <b>Ignition coil:</b> steps up voltage.",
        "<b>Contact breaker:</b> makes and breaks the primary circuit. <b>Condenser:</b> prevents arcing and helps rapid field collapse.",
        "<b>Distributor:</b> sends high voltage to correct spark plug. <b>Spark plug:</b> produces spark across electrode gap.",
        "<b>Good spark plug properties:</b> correct heat range, strong insulation, gas-tightness, resistance to fouling, corrosion and high temperature.",
    ], s["ExamBullet"])

    topic(story, 14, "Spark Plug and Fuel Injector", s, "Repeated")
    story.append(p("A spark plug is used in SI engines to ignite the compressed mixture. It consists of a centre electrode, ground electrode, insulator and metal shell. It must withstand high pressure and temperature while maintaining a reliable spark gap. A fuel injector supplies fuel in finely atomized form. In CI engines it injects diesel at high pressure near the end of compression; in modern SI engines injectors may be port type or direct injection type.", s["Body"]))

    topic(story, 15, "Condenser and Ballast Resistor", s, "Repeated")
    bullets(story, [
        "<b>Condenser:</b> connected across contact breaker points. It reduces sparking at the points and helps the ignition coil magnetic field collapse rapidly, producing high secondary voltage.",
        "<b>Ballast resistor:</b> connected in series with the ignition coil primary circuit to limit current and prevent overheating. During starting it may be bypassed to give a stronger spark.",
        "<b>Distributor:</b> routes high-voltage current to spark plugs in correct firing order and may include timing advance mechanisms.",
    ], s["ExamBullet"])

    topic(story, 16, "Wet Sump Lubrication System", s)
    story.append(p("In the wet sump system, lubricating oil is stored in the sump below the crankcase. An oil pump draws oil through a strainer and delivers it through a filter to the main oil gallery. Oil then reaches main bearings, big-end bearings, camshaft and valve gear. Splash and oil jets lubricate cylinder walls and piston pins. After lubrication and cooling, oil drains back to the sump by gravity.", s["Body"]))

    topic(story, 17, "Engine Cooling, Overcooling and Gas Temperature Curve", s, "Repeated")
    bullets(story, [
        "<b>Necessity of cooling:</b> prevents overheating, protects lubricating oil, avoids distortion/seizure, reduces knocking and maintains proper clearances.",
        "<b>Disadvantages of overcooling:</b> lower thermal efficiency, poor fuel vaporization, incomplete combustion, high oil viscosity, more friction and corrosion due to condensation.",
    ], s["ExamBullet"])
    story.append(box([
        "Gas temperature in four-stroke SI engine:",
        "  Suction: low temperature due to incoming fresh mixture.",
        "  Compression: temperature rises.",
        "  Combustion: rapid rise, maximum just after TDC.",
        "  Expansion: temperature falls as gases do work.",
        "  Exhaust: temperature falls as burnt gases leave.",
        "",
        "Temperature",
        "   ^                    peak",
        "   |                     /\\",
        "   |    compression     /  \\ expansion",
        "   |___ suction _______/    \\____ exhaust",
        "   +--------------------------------------> crank angle",
    ], code))

    topic(story, 18, "Piston/Valve Cooling and Circulation Systems", s, "Repeated")
    bullets(story, [
        "<b>Piston cooling:</b> heat leaves piston through rings to cylinder wall, by oil splash or oil jet under piston crown, and through piston pin/connecting rod.",
        "<b>Valve cooling:</b> exhaust valve loses heat mainly through valve seat to cylinder head and through valve stem to guide. Sodium-cooled hollow valves may be used.",
        "<b>Forced circulation:</b> a pump circulates coolant from radiator to engine water jackets and back; fan and radiator remove heat.",
        "<b>Thermosyphon:</b> hot water rises from engine to radiator due to lower density; cooled denser water returns to engine by natural circulation.",
    ], s["ExamBullet"])

    topic(story, 19, "Air Cooling and Cooling Fins", s, "Repeated")
    story.append(p("In air cooling, heat from cylinder and head is conducted to external fins and removed by air flowing over them. Air flow may be natural due to vehicle motion or forced by a fan and shroud. It is simple, light and avoids coolant leakage, but temperature control is less uniform than liquid cooling.", s["Body"]))
    bullets(story, [
        "<b>Types of fins:</b> annular/circumferential fins, longitudinal fins, pin fins, tapered fins, straight fins, interrupted fins and helical fins.",
        "Fins increase heat-transfer area, but spacing must be sufficient for air circulation.",
    ], s["ExamBullet"])

    topic(story, 20, "Supercharger vs Turbocharger and Wankel Engine", s, "Most Important")
    story.append(tbl([
        ["Basis", "Supercharger", "Turbocharger"],
        ["Drive", "Mechanically driven by crankshaft.", "Driven by exhaust gas turbine."],
        ["Energy", "Consumes engine power.", "Uses waste exhaust energy."],
        ["Response", "Quick response, little lag.", "May have turbo lag."],
        ["Efficiency", "Boosts power but adds mechanical loss.", "Usually improves power and efficiency."],
        ["Construction", "Belt/gear drive needed.", "Turbine and hot exhaust parts needed."],
    ], [3.3 * cm, 6.2 * cm, 6.2 * cm]))
    story.append(p("<b>Wankel engine:</b> a rotary IC engine using a triangular rotor inside an epitrochoid housing. Intake, compression, combustion/expansion and exhaust occur in separate moving chambers. It is compact and smooth but has sealing, fuel economy and emission difficulties.", s["Body"]))

    topic(story, 21, "Two-Stroke Engine and Scavenging", s, "Repeated")
    bullets(story, [
        "<b>Advantages of two-stroke engine:</b> one power stroke per revolution, high power-to-weight ratio, simple construction, low cost and more uniform torque.",
        "<b>Disadvantages:</b> imperfect scavenging, higher fuel consumption, lower efficiency, more smoke/emissions, lubrication difficulty and faster wear.",
        "<b>Scavenging:</b> removal of burnt gases and replacement by fresh charge/air. Good scavenging improves power and combustion.",
        "<b>Return-flow scavenging:</b> fresh charge moves upward, turns near head and returns downward toward exhaust port.",
        "<b>Uniflow scavenging:</b> fresh air enters from one end and exhaust leaves from the other, giving flow mainly in one direction and high scavenging efficiency.",
    ], s["ExamBullet"])

    topic(story, 22, "Engine Performance Parameters and Four-Stroke SI Engine", s)
    bullets(story, [
        "<b>Indicated power (IP):</b> power developed inside cylinder, calculated from indicated mean effective pressure.",
        "<b>Brake power (BP):</b> useful power available at crankshaft, measured by dynamometer.",
        "<b>Friction power (FP):</b> power lost in friction and auxiliaries; FP = IP - BP.",
        "<b>BSFC:</b> brake specific fuel consumption = fuel consumed per unit brake power per hour, usually kg/kWh.",
        "<b>SI vs CI:</b> SI uses spark ignition and petrol/gas fuel with lower compression ratio; CI uses compression ignition, diesel fuel and higher compression ratio.",
    ], s["ExamBullet"])
    story.append(p("A four-stroke SI engine works through suction, compression, power and exhaust strokes. Spark ignition occurs near the end of compression, and one power stroke is obtained in two crankshaft revolutions.", s["Body"]))

    topic(story, 23, "Firing Order", s, "Repeated")
    story.append(p("Firing order is the sequence in which cylinders of a multi-cylinder engine fire. It is selected to obtain uniform turning moment, better balance, reduced vibration, lower bearing load and proper cooling. Common examples are 1-3-4-2 for four-cylinder engines and 1-5-3-6-2-4 for many six-cylinder engines.", s["Body"]))

    topic(story, 24, "Flash Point and Fire Point", s, "Repeated")
    story.append(p("<b>Flash point</b> is the lowest temperature at which fuel gives off enough vapour to form an ignitable mixture and flashes momentarily when a flame is applied. <b>Fire point</b> is the lowest temperature at which the vapour continues to burn after ignition. Fire point is higher than flash point. These properties are important for safe storage, handling, transport and fuel selection.", s["Body"]))

    topic(story, 25, "Radiation Heat Transfer of an IC Engine", s)
    story.append(p("Radiation heat transfer is heat transfer by electromagnetic waves. In IC engines, high-temperature flame and combustion gases radiate heat to the piston crown, cylinder head, valves and cylinder walls. Convection is usually dominant, but radiation becomes important at high combustion temperature. Radiation depends on absolute temperature, emissivity, surface area and view factor.", s["Body"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(1.35 * cm, 0.72 * cm, "ICE MEE401 Topicwise Solved")
        canvas.drawRightString(A4[0] - 1.35 * cm, 0.72 * cm, f"Page {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUT)
