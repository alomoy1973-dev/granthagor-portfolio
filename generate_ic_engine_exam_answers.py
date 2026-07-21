from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = "IC_Engine_Exam_Answers.pdf"


def p(text, style):
    return Paragraph(text, style)


def add_bullets(story, items, style):
    for item in items:
        story.append(Paragraph(item, style, bulletText="-"))


def build_pdf():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        rightMargin=1.55 * cm,
        leftMargin=1.55 * cm,
        topMargin=1.45 * cm,
        bottomMargin=1.45 * cm,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubtitleCenter",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#374151"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Part",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.white,
            backColor=colors.HexColor("#2563eb"),
            borderPadding=(5, 4, 5, 4),
            spaceBefore=8,
            spaceAfter=9,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Question",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.8,
            leading=13.5,
            textColor=colors.HexColor("#111827"),
            spaceBefore=9,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            alignment=TA_LEFT,
            fontName="Helvetica",
            fontSize=9.4,
            leading=12.4,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ExamBullet",
            parent=styles["BodyText"],
            leftIndent=14,
            firstLineIndent=0,
            bulletIndent=5,
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.0,
            spaceAfter=2.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallHead",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=9.7,
            leading=12,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=5,
            spaceAfter=3,
        )
    )
    code = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.2,
        leading=10.2,
        leftIndent=8,
        spaceBefore=3,
        spaceAfter=5,
    )

    story = []
    story.append(p("Internal Combustion Engine: Exam Answers", styles["TitleCenter"]))
    story.append(
        p(
            "Course: MEE 401 | Based on the visible questions from the supplied examination page",
            styles["SubtitleCenter"],
        )
    )

    story.append(p("PART-A", styles["Part"]))

    story.append(p("1(a) Classify internal combustion engines on the basis of different segments.", styles["Question"]))
    story.append(p("Internal combustion engines may be classified as follows:", styles["Body"]))
    add_bullets(
        story,
        [
            "<b>According to cycle of operation:</b> Otto cycle, Diesel cycle, Dual-combustion cycle.",
            "<b>According to number of strokes:</b> four-stroke engine and two-stroke engine.",
            "<b>According to method of ignition:</b> spark ignition (SI) engine and compression ignition (CI) engine.",
            "<b>According to fuel used:</b> petrol/gasoline, diesel, gas, alcohol, hydrogen and multi-fuel engines.",
            "<b>According to cooling system:</b> air-cooled and water-cooled engines.",
            "<b>According to number and arrangement of cylinders:</b> single-cylinder or multi-cylinder; vertical, horizontal, in-line, V-type, opposed-cylinder and radial engines.",
            "<b>According to speed:</b> low-speed, medium-speed and high-speed engines.",
            "<b>According to application:</b> automobile, aircraft, marine, stationary and locomotive engines.",
            "<b>According to charging:</b> naturally aspirated, supercharged and turbocharged engines.",
        ],
        styles["ExamBullet"],
    )

    story.append(p("1(b) Explain briefly the valve timing diagram of a typical four-stroke SI engine.", styles["Question"]))
    story.append(
        p(
            "In an actual four-stroke SI engine the inlet and exhaust valves do not open and close exactly at dead centres. They are advanced or delayed to allow enough time for gas flow at high speed.",
            styles["Body"],
        )
    )
    add_bullets(
        story,
        [
            "<b>Inlet valve opens</b> about 10-20 degrees before TDC at the end of exhaust stroke. This helps fresh charge start entering as soon as suction begins.",
            "<b>Inlet valve closes</b> about 30-45 degrees after BDC. The moving charge continues to enter due to inertia, improving volumetric efficiency.",
            "<b>Spark occurs</b> about 20-35 degrees before TDC near the end of compression stroke, so that maximum pressure occurs just after TDC.",
            "<b>Exhaust valve opens</b> about 35-50 degrees before BDC near the end of power stroke. This reduces back pressure during exhaust stroke.",
            "<b>Exhaust valve closes</b> about 10-15 degrees after TDC. During this short overlap both valves remain slightly open, helping scavenging.",
        ],
        styles["ExamBullet"],
    )
    story.append(
        Preformatted(
            "Typical timing:  IVO: 10-20 deg BTDC, IVC: 30-45 deg ABDC\n"
            "                 EVO: 35-50 deg BBDC, EVC: 10-15 deg ATDC\n"
            "                 Ignition: 20-35 deg BTDC",
            code,
        )
    )

    story.append(p("2(a) Find the air-standard efficiency of a diesel engine. Why does mean effective pressure increase with initial pressure?", styles["Question"]))
    story.append(p("For an ideal Diesel cycle:", styles["Body"]))
    story.append(
        Preformatted(
            "1-2: isentropic compression\n"
            "2-3: constant-pressure heat addition\n"
            "3-4: isentropic expansion\n"
            "4-1: constant-volume heat rejection\n\n"
            "Let r = compression ratio = V1/V2\n"
            "Let rho = cut-off ratio = V3/V2\n"
            "Let k = ratio of specific heats\n\n"
            "Air-standard efficiency:\n"
            "eta_diesel = 1 - [1/(r^(k-1))] * [(rho^k - 1)/(k(rho - 1))]",
            code,
        )
    )
    story.append(
        p(
            "Mean effective pressure is the net work per cycle divided by swept volume. If the initial pressure is increased while the volume and temperature ratios are maintained, the mass of air in the cylinder increases. Since heat supplied and work done are nearly proportional to the mass of working fluid, the net work per cycle increases; therefore mean effective pressure also increases.",
            styles["Body"],
        )
    )

    story.append(p("2(b) Describe the working principle of a two-stroke SI engine with proper sketch.", styles["Question"]))
    story.append(
        p(
            "A two-stroke SI engine completes one cycle in two piston strokes, or one crankshaft revolution. It uses ports instead of separate inlet and exhaust valves in the simplest form.",
            styles["Body"],
        )
    )
    story.append(Preformatted(
        "            Spark plug\n"
        "               |\n"
        "          _____|_____\n"
        "         |           |  Exhaust port\n"
        "Transfer |  Piston   |---->\n"
        " port -->|___________|\n"
        "         | Crankcase |  Inlet from carburetor\n"
        "         |___________|<----",
        code,
    ))
    add_bullets(
        story,
        [
            "<b>Upward stroke:</b> the piston moves from BDC to TDC and compresses the charge already in the cylinder. At the same time, partial vacuum is created in the crankcase, so fresh air-fuel mixture enters through the inlet port.",
            "<b>Ignition and power:</b> near TDC the spark plug ignites the compressed mixture. The high-pressure gases push the piston downward, producing power.",
            "<b>Exhaust and transfer:</b> near BDC the exhaust port opens first and burnt gases leave. Then the transfer port opens and the compressed fresh charge from the crankcase enters the cylinder.",
            "<b>Scavenging:</b> the incoming fresh charge helps push out the remaining exhaust gases. The cycle then repeats.",
        ],
        styles["ExamBullet"],
    )

    story.append(p("3(a) A gas engine works on the constant-volume cycle. Determine salient pressures and temperatures, efficiency, work done, mean effective pressure and power.", styles["Question"]))
    story.append(p("Given: bore D = 280 mm, stroke L = 300 mm, clearance volume Vc = 1300 cm3 = 0.0013 m3, p1 = 1 bar, T1 = 28 deg C = 301 K, Tmax = T3 = 1550 deg C = 1823 K, cv = 0.718 kJ/kg K, R = 0.287 kJ/kg K, cycles/hour = 45000.", styles["Body"]))
    data = [
        ["Quantity", "Value"],
        ["Swept volume, Vs = (pi/4)D^2L", "0.01847 m3"],
        ["Total volume, V1 = Vs + Vc", "0.01977 m3"],
        ["Compression ratio, r = V1/V2", "15.21"],
        ["k = cp/cv = (cv + R)/cv", "1.40 approximately"],
    ]
    t = Table(data, colWidths=[10.0 * cm, 6.0 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5efff")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.6),
        ("LEADING", (0, 0), (-1, -1), 10.5),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9ca3af")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 5))
    story.append(Preformatted(
        "Compression, 1-2:\n"
        "T2 = T1 r^(k-1) = 301 x 15.21^0.4 = 893 K\n"
        "p2 = p1 r^k = 1 x 15.21^1.4 = 45.15 bar\n\n"
        "Constant-volume heat addition, 2-3:\n"
        "p3/T3 = p2/T2\n"
        "p3 = 45.15 x (1823/893) = 92.12 bar\n\n"
        "Expansion, 3-4:\n"
        "T4 = T3/r^(k-1) = 1823/15.21^0.4 = 614 K\n"
        "p4 = p3/r^k = 92.12/15.21^1.4 = 2.04 bar\n\n"
        "Air-standard efficiency:\n"
        "eta = 1 - 1/r^(k-1) = 1 - 1/15.21^0.4 = 0.663 = 66.3%\n\n"
        "Mass of air at state 1:\n"
        "m = p1 V1/(R T1) = (100 x 0.01977)/(0.287 x 301) = 0.02289 kg\n\n"
        "Net work per kg:\n"
        "w = cv[(T3 - T2) - (T4 - T1)]\n"
        "  = 0.718[(1823 - 893) - (614 - 301)] = 442.6 kJ/kg\n\n"
        "Work per cycle = m w = 0.02289 x 442.6 = 10.13 kJ/cycle\n"
        "Mean effective pressure = W/Vs = 10.13/0.01847 = 548 kPa = 5.48 bar\n"
        "Power = 10.13 x (45000/3600) = 126.6 kW",
        code,
    ))
    story.append(p("<b>Answer:</b> p1 = 1 bar, T1 = 301 K; p2 = 45.15 bar, T2 = 893 K; p3 = 92.12 bar, T3 = 1823 K; p4 = 2.04 bar, T4 = 614 K; efficiency = 66.3%; work per cycle = 10.13 kJ; mep = 5.48 bar; power = 126.6 kW.", styles["Body"]))

    story.append(p("3(b) Give brief description of solid fuels. Why is solid fuel not used in IC engines?", styles["Question"]))
    story.append(p("Solid fuels include coal, coke, charcoal, wood and biomass briquettes. They contain combustible elements such as carbon, hydrogen and sulphur along with moisture, ash and volatile matter. They are widely used in furnaces, boilers and gas producers, but they are not suitable for direct use in normal IC engine cylinders.", styles["Body"]))
    add_bullets(
        story,
        [
            "Solid fuel cannot be easily metered, atomized and mixed with air inside the cylinder.",
            "Combustion is slow compared with the very short time available in an IC engine.",
            "Ash and abrasive particles cause cylinder, piston-ring and valve wear.",
            "Feeding solid fuel into a sealed high-speed cylinder is mechanically difficult.",
            "Starting, load control and speed control become poor.",
            "It produces smoke, deposits and clinker, which reduce reliability.",
            "Therefore solid fuel is generally converted to producer gas first if it is to be used with an IC engine.",
        ],
        styles["ExamBullet"],
    )

    story.append(p("4(a) Briefly explain different characteristics of CI engine fuels.", styles["Question"]))
    add_bullets(
        story,
        [
            "<b>Cetane number:</b> indicates ignition quality. High cetane number gives short ignition delay and smooth diesel combustion.",
            "<b>Volatility:</b> should be sufficient for vaporization and mixing, but not so high as to cause vapour lock or unsafe handling.",
            "<b>Viscosity:</b> affects atomization and spray penetration. Too high viscosity gives poor atomization; too low viscosity causes leakage and poor lubrication of pump parts.",
            "<b>Calorific value:</b> determines heat energy available per kg of fuel.",
            "<b>Flash point and fire point:</b> important for storage and handling safety.",
            "<b>Pour point and cloud point:</b> indicate low-temperature flow properties.",
            "<b>Sulphur content:</b> should be low because sulphur forms corrosive products and increases emissions.",
            "<b>Ash and carbon residue:</b> should be low to avoid deposits, injector fouling and wear.",
            "<b>Density:</b> affects fuel quantity delivered by volume and spray characteristics.",
        ],
        styles["ExamBullet"],
    )

    story.append(p("4(b) What is engine knocking? Why does engine knock? What are octane rating and cetane rating of fuel?", styles["Question"]))
    story.append(p("<b>Engine knocking</b> is an abnormal combustion phenomenon that produces a sharp metallic sound and pressure oscillations inside the cylinder.", styles["Body"]))
    add_bullets(
        story,
        [
            "<b>In SI engines,</b> knocking occurs when the unburnt end gas auto-ignites before the normal flame front reaches it. It is promoted by high compression ratio, high charge temperature, low octane fuel, excessive spark advance, deposits and overheating.",
            "<b>In CI engines,</b> diesel knock occurs due to long ignition delay. A large amount of fuel accumulates before ignition and then burns suddenly, causing rapid pressure rise.",
            "<b>Octane rating:</b> a measure of anti-knock quality of SI engine fuel. Iso-octane is rated 100 and normal heptane is rated 0.",
            "<b>Cetane rating:</b> a measure of ignition quality of diesel fuel. Cetane is rated 100 and alpha-methyl naphthalene is commonly taken as 0 in the old reference scale.",
        ],
        styles["ExamBullet"],
    )

    story.append(PageBreak())
    story.append(p("PART-B", styles["Part"]))

    story.append(p("1(a) What are the main requirements for an ideal carburetor? Briefly explain the working principle of a simple carburetor.", styles["Question"]))
    story.append(p("An ideal carburetor should supply the correct air-fuel mixture to the engine under all operating conditions.", styles["Body"]))
    add_bullets(
        story,
        [
            "It should give rich mixture for starting and acceleration.",
            "It should give nearly stoichiometric mixture for normal running.",
            "It should give lean mixture for economical cruising.",
            "It should maintain correct mixture over a wide range of speed and load.",
            "It should provide good atomization and uniform distribution of fuel.",
            "It should respond quickly to throttle movement.",
            "It should be simple, reliable, compact and easy to adjust.",
        ],
        styles["ExamBullet"],
    )
    story.append(p("<b>Working principle:</b> In a simple carburetor, air passes through a venturi. The air velocity increases at the throat and pressure falls below atmospheric pressure. This pressure difference draws petrol from the float chamber through the fuel jet. Fuel is atomized into the air stream and the mixture flows to the engine through the throttle valve. The float chamber keeps the fuel level almost constant.", styles["Body"]))

    story.append(p("1(b) What are concentric and eccentric carburetors? Briefly explain magneto ignition system.", styles["Question"]))
    add_bullets(
        story,
        [
            "<b>Concentric carburetor:</b> the fuel jet is placed approximately at the centre line of the venturi throat. The air flow surrounds the jet symmetrically, giving uniform mixture formation.",
            "<b>Eccentric carburetor:</b> the fuel jet is placed away from the centre line of the venturi. It may be used to suit space, flow direction or constructional requirements.",
            "<b>Magneto ignition:</b> this system produces ignition current by rotating a permanent magnet or armature. It does not require a battery during running. The magneto generates low-voltage current, the contact breaker interrupts the primary circuit, and the high-voltage secondary current is sent through the distributor to the spark plug. It is common in small engines, motorcycles and aircraft engines because it is self-contained and reliable.",
        ],
        styles["ExamBullet"],
    )

    story.append(p("2(a) Mention some disadvantages of engine overcooling. Explain briefly gas temperature variation curve for a typical four-stroke SI engine.", styles["Question"]))
    story.append(p("<b>Disadvantages of overcooling:</b>", styles["Body"]))
    add_bullets(
        story,
        [
            "Thermal efficiency decreases because more heat is lost to the cooling system.",
            "Fuel vaporization becomes poor, causing incomplete combustion and high fuel consumption.",
            "Lubricating oil becomes more viscous, increasing friction loss.",
            "Acidic products may condense on cylinder walls and cause corrosion.",
            "Piston, rings and cylinder wear increase due to poor lubrication.",
            "Engine warm-up becomes slow and power output may fall.",
        ],
        styles["ExamBullet"],
    )
    story.append(p("<b>Gas temperature variation:</b> During suction, cylinder gas temperature is low because fresh mixture enters. During compression, temperature rises. After ignition near the end of compression, combustion causes a rapid rise and maximum temperature occurs just after TDC. During expansion, temperature falls as gases do work on the piston. During exhaust, the temperature continues to decrease as burnt gases leave the cylinder.", styles["Body"]))
    story.append(Preformatted(
        "Temperature\n"
        "   ^                 peak after TDC\n"
        "   |                /\\\n"
        "   |               /  \\ expansion\n"
        "   | compression  /    \\____ exhaust\n"
        "   |____ suction_/            \n"
        "   +--------------------------------> crank angle",
        code,
    ))

    story.append(p("2(b) How can a valve be cooled? How does thermosyphon circulation system work?", styles["Question"]))
    add_bullets(
        story,
        [
            "Exhaust valves are cooled mainly by heat conduction from valve head to valve seat and then to the water jacket.",
            "Heat also flows through the valve stem to the valve guide.",
            "Sodium-cooled hollow valves may be used in high-output engines. Sodium melts and transfers heat from the hot head to the cooler stem.",
            "Correct valve seating, suitable materials, water jackets near the valve seat and adequate lubrication help valve cooling.",
        ],
        styles["ExamBullet"],
    )
    story.append(p("<b>Thermosyphon system:</b> It is a natural circulation water-cooling system. Water in the engine jacket absorbs heat, becomes lighter and rises to the top tank of the radiator. In the radiator it loses heat to air, becomes cooler and denser, and flows down to the bottom tank. The cool water then enters the engine jacket again. Circulation occurs due to density difference; no water pump is required.", styles["Body"]))

    story.append(p("3(a) What is Wankel engine? Mention the difference between supercharger and turbocharger.", styles["Question"]))
    story.append(p("<b>Wankel engine:</b> A Wankel engine is a rotary internal combustion engine in which a triangular rotor moves inside an epitrochoid-shaped housing. The spaces between the rotor and housing successively perform intake, compression, combustion/expansion and exhaust. It has few moving parts, compact size and smooth operation, but sealing and fuel economy can be challenging.", styles["Body"]))
    comparison = [
        ["Point", "Supercharger", "Turbocharger"],
        ["Drive", "Driven mechanically by crankshaft", "Driven by exhaust gas turbine"],
        ["Power use", "Consumes engine power directly", "Uses waste exhaust energy"],
        ["Response", "Quick response, little lag", "May have turbo lag"],
        ["Efficiency", "Lower than turbocharger at many conditions", "Usually improves overall efficiency"],
        ["Complexity/heat", "Mechanically simpler, less exhaust heat", "Hotter and needs turbine/compressor matching"],
    ]
    tbl = Table(comparison, colWidths=[3.4 * cm, 6.1 * cm, 6.1 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5efff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.1),
        ("LEADING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9ca3af")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tbl)

    story.append(p("3(b) Briefly explain return-flow scavenging. What is uniflow scavenging?", styles["Question"]))
    add_bullets(
        story,
        [
            "<b>Return-flow scavenging:</b> In this two-stroke scavenging method, transfer and exhaust ports are on the same side or arranged so that fresh charge first moves upward, turns near the cylinder head, and then flows downward toward the exhaust port. The deflector piston may be used to guide the flow and reduce short-circuiting.",
            "<b>Uniflow scavenging:</b> In uniflow scavenging, fresh air enters from ports near one end of the cylinder and exhaust gases leave from the other end, usually through exhaust valves in the cylinder head. The gas flow is mainly in one direction, giving better scavenging efficiency and less mixing.",
        ],
        styles["ExamBullet"],
    )

    story.append(p("4. Write down short note on the following.", styles["Question"]))
    story.append(p("(a) Ballast resistor and distributor.", styles["SmallHead"]))
    story.append(p("A ballast resistor is connected in series with the ignition coil primary circuit to limit current and protect the coil and contact breaker. During starting it may be bypassed to give a stronger spark. A distributor routes the high-voltage current from the ignition coil to the correct spark plug in the proper firing order. It also contains or works with timing advance mechanisms.", styles["Body"]))
    story.append(p("(b) Firing order.", styles["SmallHead"]))
    story.append(p("Firing order is the sequence in which the cylinders of a multi-cylinder engine fire. It is selected to obtain smooth running, uniform power impulses, reduced vibration, lower bearing load and proper crankshaft balance. Common examples are 1-3-4-2 for a four-cylinder engine and 1-5-3-6-2-4 for many six-cylinder engines.", styles["Body"]))
    story.append(p("(c) Spark plug and fuel injector.", styles["SmallHead"]))
    story.append(p("A spark plug is used in SI engines to ignite the compressed air-fuel mixture by producing an electric spark across its electrodes. It must withstand high temperature and pressure and remove heat through its body. A fuel injector delivers fuel into the intake port or combustion chamber in a fine spray. In CI engines it injects diesel at high pressure near the end of compression so that atomization, penetration and distribution are suitable for combustion.", styles["Body"]))
    story.append(p("(d) Flash point and fire point.", styles["SmallHead"]))
    story.append(p("Flash point is the lowest temperature at which a fuel gives off enough vapour to form an ignitable mixture with air and flashes momentarily when a flame is applied. Fire point is the lowest temperature at which the vapour continues to burn for a short time after ignition. Fire point is higher than flash point.", styles["Body"]))
    story.append(p("(e) Radiation heat transfer of an IC engine.", styles["SmallHead"]))
    story.append(p("Radiation heat transfer is the transfer of heat by electromagnetic waves from hot engine parts and combustion gases to cooler surroundings or walls. In IC engines, radiation from the high-temperature flame and gases to the cylinder head, piston crown and liner is less dominant than convection but becomes important at high combustion temperatures. Radiative heat loss depends on absolute temperature, surface area, emissivity and view factor.", styles["Body"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6b7280"))
        canvas.drawString(1.55 * cm, 0.9 * cm, "IC Engine Exam Answers")
        canvas.drawRightString(A4[0] - 1.55 * cm, 0.9 * cm, f"Page {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_pdf()
    print(OUT)
