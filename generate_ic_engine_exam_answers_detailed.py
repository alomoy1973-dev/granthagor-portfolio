from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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


OUT = "IC_Engine_Exam_Answers_Detailed.pdf"


def para(text, style):
    return Paragraph(text, style)


def bullets(story, items, style):
    for item in items:
        story.append(Paragraph(item, style, bulletText="-"))


def q(story, text, styles):
    story.append(Paragraph(text, styles["Question"]))


def formula_box(lines, code_style):
    return KeepTogether([
        Preformatted("\n".join(lines), code_style),
        Spacer(1, 4),
    ])


def result_table(rows, widths):
    table = Table(rows, colWidths=widths, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.4),
        ("LEADING", (0, 0), (-1, -1), 10.4),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#93a4b7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.35 * cm,
    )

    base = getSampleStyleSheet()
    base.add(ParagraphStyle(
        name="TitleCenter", parent=base["Title"], alignment=TA_CENTER,
        fontName="Helvetica-Bold", fontSize=16.5, leading=20,
        textColor=colors.HexColor("#172554"), spaceAfter=5,
    ))
    base.add(ParagraphStyle(
        name="SubCenter", parent=base["Normal"], alignment=TA_CENTER,
        fontSize=9.4, leading=12, textColor=colors.HexColor("#374151"),
        spaceAfter=13,
    ))
    base.add(ParagraphStyle(
        name="Part", parent=base["Heading1"], alignment=TA_CENTER,
        fontName="Helvetica-Bold", fontSize=13.2, leading=16.5,
        textColor=colors.white, backColor=colors.HexColor("#1d4ed8"),
        borderPadding=(5, 4, 5, 4), spaceBefore=8, spaceAfter=9,
    ))
    base.add(ParagraphStyle(
        name="Question", parent=base["Heading2"], fontName="Helvetica-Bold",
        fontSize=10.6, leading=13.4, textColor=colors.HexColor("#111827"),
        spaceBefore=9, spaceAfter=4, keepWithNext=True,
    ))
    base.add(ParagraphStyle(
        name="Body", parent=base["BodyText"], alignment=TA_LEFT,
        fontName="Helvetica", fontSize=9.25, leading=12.2, spaceAfter=4.2,
    ))
    base.add(ParagraphStyle(
        name="ExamBullet", parent=base["BodyText"], leftIndent=14,
        firstLineIndent=0, bulletIndent=5, fontName="Helvetica",
        fontSize=9.05, leading=11.8, spaceAfter=2.5,
    ))
    base.add(ParagraphStyle(
        name="SubHead", parent=base["Heading3"], fontName="Helvetica-Bold",
        fontSize=9.65, leading=12, textColor=colors.HexColor("#1f2937"),
        spaceBefore=5, spaceAfter=3,
    ))
    code = ParagraphStyle(
        "MathBox", parent=base["Code"], fontName="Courier", fontSize=8.35,
        leading=10.7, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=5,
        borderWidth=0.45, borderColor=colors.HexColor("#bfdbfe"),
        borderPadding=6, backColor=colors.HexColor("#f8fbff"),
    )

    story = []
    story.append(para("Internal Combustion Engine: Detailed Exam Answers", base["TitleCenter"]))
    story.append(para("Course: MEE 401 | University-exam style answer sheet from the supplied question page", base["SubCenter"]))
    story.append(para("PART-A", base["Part"]))

    q(story, "1(a) Classify internal combustion engines on the basis of different segments.", base)
    story.append(para("Internal combustion engines are classified into different groups because their construction, method of combustion, fuel system, cooling method and field of application are not the same. A complete classification is given below.", base["Body"]))
    bullets(story, [
        "<b>According to thermodynamic cycle:</b> Otto cycle engine, Diesel cycle engine and Dual-combustion cycle engine. SI petrol engines are generally represented by the Otto cycle, while CI engines are represented by the Diesel or Dual cycle.",
        "<b>According to number of strokes per cycle:</b> four-stroke engines and two-stroke engines. A four-stroke engine completes one cycle in two crankshaft revolutions, whereas a two-stroke engine completes one cycle in one crankshaft revolution.",
        "<b>According to method of ignition:</b> spark ignition (SI) engine and compression ignition (CI) engine. In SI engines a spark plug starts combustion; in CI engines the high temperature of compressed air ignites the injected fuel.",
        "<b>According to fuel used:</b> petrol, diesel, gas, alcohol, kerosene, hydrogen and multi-fuel engines. The fuel decides the fuel supply system, compression ratio and ignition method.",
        "<b>According to cooling method:</b> air-cooled and water-cooled engines. Cooling is necessary to keep the cylinder, piston, valves and lubricating oil within safe temperature limits.",
        "<b>According to cylinder number and arrangement:</b> single-cylinder and multi-cylinder engines; in-line, V-type, opposed-cylinder, radial, vertical and horizontal engines.",
        "<b>According to speed:</b> low-speed, medium-speed and high-speed engines. Large marine engines are usually low-speed, while automotive petrol engines are high-speed.",
        "<b>According to air charging:</b> naturally aspirated, supercharged and turbocharged engines. Supercharging increases the mass of air supplied to the cylinder.",
        "<b>According to application:</b> automobile, aircraft, marine, locomotive, stationary and power-plant engines.",
    ], base["ExamBullet"])

    q(story, "1(b) Explain briefly the valve timing diagram of a typical four-stroke SI engine.", base)
    story.append(para("In the theoretical four-stroke cycle the inlet and exhaust valves open and close exactly at TDC and BDC. In a real high-speed engine this is not possible because air and exhaust gases require finite time to flow. Therefore the valves are opened early and closed late. This actual timing improves breathing, reduces pumping loss and increases volumetric efficiency.", base["Body"]))
    bullets(story, [
        "<b>Inlet valve opening (IVO):</b> The inlet valve opens about 10 to 20 degrees before TDC near the end of the exhaust stroke. This early opening allows the fresh charge to start entering as soon as the piston begins the suction stroke.",
        "<b>Inlet valve closing (IVC):</b> The inlet valve closes about 30 to 45 degrees after BDC. Although the piston has started moving upward, the inertia of the incoming charge continues to fill the cylinder.",
        "<b>Ignition advance:</b> The spark is produced about 20 to 35 degrees before TDC near the end of the compression stroke. This is necessary because combustion takes a short but finite time.",
        "<b>Exhaust valve opening (EVO):</b> The exhaust valve opens about 35 to 50 degrees before BDC during the power stroke. This releases much of the exhaust pressure before the piston starts the exhaust stroke.",
        "<b>Exhaust valve closing (EVC):</b> The exhaust valve closes about 10 to 15 degrees after TDC. The short period when both valves are open is called valve overlap and it helps remove burnt gases.",
    ], base["ExamBullet"])
    story.append(formula_box([
        "Typical SI engine valve timing:",
        "  IVO = 10-20 deg before TDC       IVC = 30-45 deg after BDC",
        "  EVO = 35-50 deg before BDC       EVC = 10-15 deg after TDC",
        "  Spark advance = 20-35 deg before TDC",
    ], code))

    q(story, "2(a) Find out air-standard efficiency of a diesel engine. Why does mean effective pressure increase with the increase of initial pressure?", base)
    story.append(para("The air-standard Diesel cycle consists of isentropic compression, constant-pressure heat addition, isentropic expansion and constant-volume heat rejection. Air is assumed to be the working fluid throughout the cycle.", base["Body"]))
    story.append(formula_box([
        "For Diesel cycle:",
        "  r   = compression ratio = V1/V2",
        "  rho = cut-off ratio     = V3/V2",
        "  k   = ratio of specific heats",
        "",
        "Thermal efficiency:",
        "                 1        (rho^k - 1)",
        "  eta_d = 1 - --------- x ----------------",
        "              r^(k-1)     k(rho - 1)",
    ], code))
    story.append(para("Thus, Diesel cycle efficiency increases when compression ratio increases and decreases when the cut-off ratio increases. For the same compression ratio, an Otto cycle has higher efficiency than a Diesel cycle, but the Diesel engine can safely use a much higher compression ratio.", base["Body"]))
    story.append(para("<b>Effect of initial pressure on mean effective pressure:</b> Mean effective pressure is the hypothetical constant pressure which, if it acted on the piston during the power stroke, would produce the same net work as the actual cycle. Mathematically, <b>mep = net work per cycle / swept volume</b>. If the initial pressure is increased while the initial temperature and volume are unchanged, the mass of air inside the cylinder increases according to pV = mRT. More air permits more fuel to burn, so the heat supplied and net work per cycle increase. Since swept volume remains the same, mean effective pressure increases.", base["Body"]))

    q(story, "2(b) Describe the working principle of a two-stroke SI engine with proper sketch.", base)
    story.append(para("A two-stroke SI engine completes the whole cycle in two strokes of the piston, namely one upward stroke and one downward stroke. Therefore one power stroke is obtained in every crankshaft revolution. In the simplest engine, inlet, transfer and exhaust ports are opened and closed by the movement of the piston.", base["Body"]))
    story.append(formula_box([
        "Simplified sketch:",
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
        "<b>Upward stroke:</b> The piston moves from BDC to TDC. The charge already present in the cylinder is compressed. At the same time, the upward motion creates a partial vacuum in the crankcase, so fresh air-fuel mixture enters the crankcase through the inlet port.",
        "<b>Ignition:</b> Near the end of compression the spark plug ignites the compressed charge. Combustion raises the pressure and temperature of the gases.",
        "<b>Downward or power stroke:</b> The high-pressure gases push the piston downward and useful work is produced. During this downward motion the fresh charge in the crankcase is compressed.",
        "<b>Exhaust and transfer:</b> Near BDC the exhaust port opens first and burnt gases leave. Soon after, the transfer port opens and the compressed fresh charge from the crankcase enters the cylinder.",
        "<b>Scavenging:</b> The entering fresh charge helps push the remaining exhaust gas out of the cylinder. Some loss of fresh charge may occur, which is one disadvantage of the simple two-stroke SI engine.",
    ], base["ExamBullet"])

    q(story, "3(a) A gas engine works on the constant-volume cycle. Determine the salient pressures and temperatures, air-standard efficiency, work done, mean effective pressure and power.", base)
    story.append(para("This is an air-standard constant-volume cycle, that is an Otto cycle. The solution is arranged in a step-by-step form for clarity.", base["Body"]))
    story.append(result_table([
        ["Given data", "Value"],
        ["Bore, D", "280 mm = 0.28 m"],
        ["Stroke, L", "300 mm = 0.30 m"],
        ["Clearance volume, Vc", "1300 cm3 = 0.0013 m3"],
        ["Initial pressure, p1", "1 bar = 100 kPa"],
        ["Initial temperature, T1", "28 deg C = 301 K"],
        ["Maximum temperature, T3", "1550 deg C = 1823 K"],
        ["cv and R", "0.718 kJ/kg K and 0.287 kJ/kg K"],
        ["Working cycles per hour", "45000"],
    ], [6.5 * cm, 9.4 * cm]))
    story.append(Spacer(1, 5))
    story.append(formula_box([
        "Step 1: Volumes and compression ratio",
        "  Vs = (pi/4)D^2L",
        "     = (pi/4)(0.28)^2(0.30)",
        "     = 0.01847 m3",
        "",
        "  V1 = Vs + Vc = 0.01847 + 0.00130 = 0.01977 m3",
        "  V2 = Vc = 0.00130 m3",
        "",
        "  r = V1/V2 = 0.01977/0.00130 = 15.21",
    ], code))
    story.append(formula_box([
        "Step 2: Ratio of specific heats",
        "  cp = cv + R = 0.718 + 0.287 = 1.005 kJ/kg K",
        "  k  = cp/cv = 1.005/0.718 = 1.40 approximately",
    ], code))
    story.append(formula_box([
        "Step 3: Isentropic compression, 1-2",
        "  T2 = T1 x r^(k-1)",
        "     = 301 x 15.21^0.4",
        "     = 893 K",
        "",
        "  p2 = p1 x r^k",
        "     = 1 x 15.21^1.4",
        "     = 45.15 bar",
    ], code))
    story.append(formula_box([
        "Step 4: Constant-volume heat addition, 2-3",
        "  Since volume is constant, p/T = constant.",
        "",
        "  p3/p2 = T3/T2",
        "  p3 = p2 x (T3/T2)",
        "     = 45.15 x (1823/893)",
        "     = 92.12 bar",
    ], code))
    story.append(formula_box([
        "Step 5: Isentropic expansion, 3-4",
        "  T4 = T3/r^(k-1)",
        "     = 1823/15.21^0.4",
        "     = 614 K",
        "",
        "  p4 = p3/r^k",
        "     = 92.12/15.21^1.4",
        "     = 2.04 bar",
    ], code))
    story.append(formula_box([
        "Step 6: Air-standard efficiency",
        "  eta = 1 - 1/r^(k-1)",
        "      = 1 - 1/15.21^0.4",
        "      = 0.663",
        "      = 66.3 percent",
    ], code))
    story.append(formula_box([
        "Step 7: Work done and power",
        "  Mass of air:",
        "  m = p1V1/(RT1)",
        "    = (100 x 0.01977)/(0.287 x 301)",
        "    = 0.02289 kg",
        "",
        "  Net work per kg:",
        "  w = cv[(T3 - T2) - (T4 - T1)]",
        "    = 0.718[(1823 - 893) - (614 - 301)]",
        "    = 442.6 kJ/kg",
        "",
        "  Work per cycle = m x w",
        "                 = 0.02289 x 442.6",
        "                 = 10.13 kJ/cycle",
        "",
        "  Mean effective pressure:",
        "  mep = Work per cycle / swept volume",
        "      = 10.13/0.01847",
        "      = 548 kPa = 5.48 bar",
        "",
        "  Power = Work per cycle x cycles per second",
        "        = 10.13 x (45000/3600)",
        "        = 126.6 kW",
    ], code))
    story.append(result_table([
        ["Final result", "Answer"],
        ["Compression ratio", "15.21"],
        ["State 2", "p2 = 45.15 bar, T2 = 893 K"],
        ["State 3", "p3 = 92.12 bar, T3 = 1823 K"],
        ["State 4", "p4 = 2.04 bar, T4 = 614 K"],
        ["Air-standard efficiency", "66.3 percent"],
        ["Work done per cycle", "10.13 kJ"],
        ["Mean effective pressure", "5.48 bar"],
        ["Power developed", "126.6 kW"],
    ], [6.5 * cm, 9.4 * cm]))

    q(story, "3(b) Give brief description of solid fuels. Why is solid fuel not used in IC engines?", base)
    story.append(para("Solid fuels are fuels which remain in solid form at ordinary temperature and pressure. Examples are coal, coke, charcoal, wood, peat and biomass briquettes. Their important constituents are carbon, hydrogen, oxygen, sulphur, moisture, volatile matter and ash. Coal is the most important industrial solid fuel and is graded according to carbon content, moisture, ash and calorific value.", base["Body"]))
    story.append(para("In IC engines, combustion has to be completed within a very short time and the fuel must be supplied in a controlled and finely divided form. Direct use of solid fuel does not satisfy these requirements.", base["Body"]))
    bullets(story, [
        "Solid fuel cannot be injected, atomized and mixed with air as easily as liquid or gaseous fuel.",
        "Its combustion rate is slow; therefore complete combustion within the engine cylinder is difficult.",
        "Ash causes deposits, abrasion and wear of piston rings, cylinder liner, valves and exhaust passages.",
        "Fuel feeding and quantity control are mechanically difficult in a high-speed closed cylinder.",
        "Starting, acceleration and load control become poor.",
        "Smoke, clinker formation and carbon deposits reduce reliability.",
        "For this reason solid fuels are generally converted into producer gas before being used in gas engines.",
    ], base["ExamBullet"])

    q(story, "4(a) Briefly explain different characteristics of CI engine fuels.", base)
    story.append(para("CI engine fuel must ignite readily after injection into hot compressed air, burn smoothly and leave minimum deposits. The following properties are important for diesel fuel selection.", base["Body"]))
    bullets(story, [
        "<b>Cetane number:</b> It indicates ignition quality. A higher cetane number means shorter ignition delay and smoother running.",
        "<b>Volatility:</b> The fuel should vaporize sufficiently for good mixing, but excessive volatility may create handling and vapour problems.",
        "<b>Viscosity:</b> It affects atomization, spray penetration and leakage in the injection pump. Very high viscosity gives coarse spray, while very low viscosity gives poor lubrication.",
        "<b>Calorific value:</b> It is the heat released by complete combustion of unit mass of fuel. Higher calorific value generally gives higher power for the same fuel mass.",
        "<b>Flash point:</b> It is important for safe storage and transportation. Diesel fuel should have a reasonably high flash point.",
        "<b>Cloud point and pour point:</b> These indicate low-temperature flow behaviour. Low values are desirable in cold weather.",
        "<b>Sulphur content:</b> Sulphur should be low because it forms corrosive acids and increases harmful emissions.",
        "<b>Ash and carbon residue:</b> These should be low to reduce injector fouling, deposits and wear.",
        "<b>Density:</b> Density affects the amount of fuel delivered by volume and also influences spray characteristics.",
    ], base["ExamBullet"])

    q(story, "4(b) What is engine knocking? Why does engine knock? What are octane rating and cetane rating of fuel?", base)
    story.append(para("Engine knocking is an abnormal combustion phenomenon in which pressure waves are produced inside the cylinder and a sharp metallic sound is heard. It reduces power, increases heat transfer, causes vibration and may damage piston, rings, bearings and cylinder head.", base["Body"]))
    bullets(story, [
        "<b>Knock in SI engine:</b> In a petrol engine, the spark starts a normal flame front. If the unburnt end gas ahead of this flame becomes too hot and auto-ignites, sudden pressure rise occurs. This is called detonation or SI engine knock.",
        "<b>Causes in SI engine:</b> high compression ratio, low octane fuel, high inlet air temperature, excessive spark advance, hot deposits, overheated spark plug and poor combustion chamber design.",
        "<b>Knock in CI engine:</b> In a diesel engine, knock occurs mainly because of long ignition delay. During the delay period, fuel accumulates in the cylinder. When ignition begins, a large amount of fuel burns suddenly and causes rapid pressure rise.",
        "<b>Octane rating:</b> Octane number measures the anti-knock quality of SI engine fuel. Iso-octane is assigned 100 and normal heptane is assigned 0. A petrol of 80 octane behaves like a mixture of 80 percent iso-octane and 20 percent normal heptane in the standard test engine.",
        "<b>Cetane rating:</b> Cetane number measures the ignition quality of diesel fuel. A higher cetane number means shorter ignition delay. Cetane is assigned 100 and alpha-methyl naphthalene is taken as 0 in the older reference scale.",
    ], base["ExamBullet"])

    story.append(PageBreak())
    story.append(para("PART-B", base["Part"]))

    q(story, "1(a) What are the main requirements for an ideal carburetor? Briefly explain the working principle of a simple carburetor.", base)
    story.append(para("A carburetor is used in a conventional SI engine to prepare a combustible air-fuel mixture and supply it to the engine according to speed and load. An ideal carburetor should automatically supply the correct mixture under every operating condition.", base["Body"]))
    bullets(story, [
        "It should supply a rich mixture during starting because some fuel condenses on cold walls.",
        "It should provide a slightly rich mixture during acceleration and full-load operation to obtain maximum power.",
        "It should provide a comparatively lean mixture during cruising for better fuel economy.",
        "It should maintain the correct air-fuel ratio over a wide range of engine speed and throttle opening.",
        "It should ensure good atomization and vaporization of fuel.",
        "It should distribute mixture uniformly to all cylinders.",
        "It should be simple, reliable, cheap, compact and easy to adjust.",
    ], base["ExamBullet"])
    story.append(para("<b>Working principle of simple carburetor:</b> Air from the atmosphere flows through a venturi. At the venturi throat, air velocity increases and pressure decreases. The float chamber maintains fuel at an almost constant level. Because the pressure at the fuel jet is lower than the pressure in the float chamber, petrol is discharged through the jet into the air stream. The fuel breaks into small droplets, mixes with air and forms a combustible mixture. The throttle valve controls the quantity of mixture supplied to the engine, and hence controls engine power.", base["Body"]))

    q(story, "1(b) What are concentric and eccentric carburetors? Briefly explain magneto ignition system.", base)
    story.append(para("<b>Concentric carburetor:</b> In a concentric carburetor the fuel jet is placed approximately on the centre line of the air passage or venturi. The air flow around the jet is symmetrical, so mixture formation is comparatively uniform.", base["Body"]))
    story.append(para("<b>Eccentric carburetor:</b> In an eccentric carburetor the fuel jet is placed away from the centre line of the venturi. This arrangement may be used because of constructional convenience, space limitation or required flow pattern.", base["Body"]))
    story.append(para("<b>Magneto ignition system:</b> A magneto ignition system is a self-contained ignition system which generates its own electric current. A permanent magnet and armature are rotated so that current is induced in the primary winding. When the contact breaker opens, the primary current is interrupted and a high voltage is induced in the secondary winding. This high voltage is distributed to the proper spark plug through the distributor. Since it does not require a battery during running, it is widely used in motorcycles, small engines and aircraft engines.", base["Body"]))

    q(story, "2(a) Mention some disadvantages of engine overcooling. Explain briefly gas temperature variation curve for a typical four-stroke SI engine.", base)
    story.append(para("The cooling system should remove only the excess heat from the engine. If too much heat is removed, the engine becomes overcooled and several harmful effects occur.", base["Body"]))
    bullets(story, [
        "Thermal efficiency decreases because a larger fraction of heat is rejected to the cooling water or air.",
        "Fuel vaporization becomes poor, especially during starting and low-load operation.",
        "Combustion may become incomplete, increasing fuel consumption and carbon deposits.",
        "Lubricating oil becomes too viscous, so friction loss and wear increase.",
        "Water vapour and acidic products may condense on cylinder walls and cause corrosion.",
        "Engine warm-up time increases and useful power output may decrease.",
    ], base["ExamBullet"])
    story.append(para("<b>Gas temperature variation in four-stroke SI engine:</b> During the suction stroke the temperature of the gas in the cylinder is comparatively low because fresh air-fuel mixture enters. During compression, temperature rises due to compression. Near the end of compression, the spark is produced. Combustion continues slightly after TDC and the gas temperature rises rapidly to a maximum just after TDC. During the expansion stroke the gas does work on the piston, so temperature falls. During exhaust, hot gases leave the cylinder and the temperature further decreases.", base["Body"]))
    story.append(formula_box([
        "Qualitative temperature-crank angle curve:",
        "",
        "Temperature",
        "   ^                      Maximum after TDC",
        "   |                         /\\",
        "   |                        /  \\",
        "   |       Compression     /    \\  Expansion",
        "   |      ________________/      \\_______ Exhaust",
        "   |_____/  Suction",
        "   +------------------------------------------------> Crank angle",
    ], code))

    q(story, "2(b) How can a valve be cooled? How does thermosyphon circulation system work?", base)
    story.append(para("<b>Valve cooling:</b> The exhaust valve is one of the hottest parts of an IC engine because it is exposed to hot burnt gases. It is cooled mainly by conduction through the valve seat and valve stem.", base["Body"]))
    bullets(story, [
        "When the valve is closed, heat flows from the valve head to the valve seat and then to the cylinder head and cooling water jacket.",
        "Some heat also flows through the valve stem to the valve guide.",
        "Correct valve seating is very important because poor contact reduces heat transfer.",
        "High-temperature valve materials and suitable valve clearances are used to prevent burning.",
        "In heavy-duty engines, hollow sodium-cooled valves may be used. Sodium melts during operation and carries heat from the valve head to the valve stem.",
    ], base["ExamBullet"])
    story.append(para("<b>Thermosyphon circulation:</b> Thermosyphon is a natural water-circulation cooling system. Water in the cylinder jacket absorbs heat from the engine and becomes lighter. This hot water rises to the upper tank of the radiator. In the radiator it loses heat to the surrounding air, becomes cooler and denser, and flows down to the lower tank. From the lower tank, the cool water returns to the engine jacket. Thus circulation takes place automatically because of density difference; no pump is required.", base["Body"]))

    q(story, "3(a) What is Wankel engine? Mention the difference between supercharger and turbocharger.", base)
    story.append(para("<b>Wankel engine:</b> A Wankel engine is a rotary internal combustion engine. Instead of a reciprocating piston, it uses a roughly triangular rotor rotating inside an epitrochoid-shaped housing. The spaces between the rotor and housing form working chambers. As the rotor moves, intake, compression, combustion/expansion and exhaust occur successively. The engine is compact, light and smooth because it has fewer reciprocating parts, but sealing, emissions and fuel consumption are common difficulties.", base["Body"]))
    story.append(result_table([
        ["Basis", "Supercharger", "Turbocharger"],
        ["Driving method", "Driven mechanically by crankshaft through belt, gear or chain.", "Driven by exhaust gas through a turbine."],
        ["Energy source", "Uses part of engine brake power.", "Uses energy that would otherwise leave with exhaust gas."],
        ["Response", "Quick response and little lag.", "May suffer from turbo lag at low speed."],
        ["Efficiency", "Increases power but consumes mechanical power.", "Usually improves overall efficiency and power output."],
        ["Construction", "Mechanically simpler but requires drive arrangement.", "Requires turbine, compressor, high-temperature materials and lubrication."],
        ["Use", "Used where immediate boost is important.", "Widely used in modern diesel and petrol engines for better power and economy."],
    ], [3.4 * cm, 6.2 * cm, 6.2 * cm]))

    q(story, "3(b) Briefly explain return-flow scavenging. What is uniflow scavenging?", base)
    story.append(para("<b>Return-flow scavenging:</b> Return-flow scavenging is used in some two-stroke engines. In this method the fresh charge enters the cylinder through transfer ports and is directed upward. It then turns near the cylinder head and flows back downward toward the exhaust port. A deflector piston may be used to guide the fresh charge so that it does not directly escape through the exhaust port. The purpose is to remove burnt gases and fill the cylinder with fresh charge.", base["Body"]))
    story.append(para("<b>Uniflow scavenging:</b> In uniflow scavenging the fresh air enters at one end of the cylinder and exhaust gases leave from the other end. Usually air enters through ports near the bottom of the cylinder and exhaust leaves through valves in the cylinder head. Since the gas flow is mainly in one direction, mixing between fresh charge and exhaust gas is reduced and scavenging efficiency is high.", base["Body"]))

    q(story, "4. Write down short note on the following.", base)
    story.append(para("(a) Ballast resistor and distributor.", base["SubHead"]))
    story.append(para("A ballast resistor is connected in series with the primary circuit of an ignition coil. Its function is to limit current through the coil and contact breaker during normal running, thereby preventing overheating. During starting, the resistor may be bypassed so that the coil receives higher voltage and produces a stronger spark. A distributor receives the high-voltage current from the ignition coil and sends it to the spark plugs in the correct firing order. It also helps maintain correct ignition timing with the help of advance mechanisms.", base["Body"]))
    story.append(para("(b) Firing order.", base["SubHead"]))
    story.append(para("Firing order is the sequence in which the cylinders of a multi-cylinder engine produce power strokes. A proper firing order is chosen to obtain uniform turning effort, reduce vibration, avoid excessive bearing load and improve engine balance. For example, a common four-cylinder firing order is 1-3-4-2, while many six-cylinder engines use 1-5-3-6-2-4.", base["Body"]))
    story.append(para("(c) Spark plug and fuel injector.", base["SubHead"]))
    story.append(para("A spark plug is used in an SI engine to ignite the compressed air-fuel mixture. It has a central electrode, ground electrode, ceramic insulator and metal shell. A high voltage produces a spark across the electrode gap. A fuel injector is used to deliver fuel in a fine spray. In CI engines, the injector sprays diesel into the combustion chamber at high pressure near the end of compression. Good atomization, penetration and distribution are essential for proper combustion.", base["Body"]))
    story.append(para("(d) Flash point and fire point.", base["SubHead"]))
    story.append(para("Flash point is the lowest temperature at which a fuel gives off sufficient vapour to form an ignitable mixture with air and gives a momentary flash when a flame is applied. Fire point is the lowest temperature at which the fuel vapour continues to burn for at least a short time after ignition. Fire point is always higher than flash point. These properties are important for safe storage, handling and transport of fuels.", base["Body"]))
    story.append(para("(e) Radiation heat transfer of an IC engine.", base["SubHead"]))
    story.append(para("Radiation heat transfer is the transfer of heat by electromagnetic waves. In an IC engine, high-temperature flame and combustion gases radiate heat to the piston crown, cylinder head, valves and cylinder walls. Although convection is usually the major mode of heat transfer in the cylinder, radiation becomes important at very high gas temperature. Radiation heat transfer depends on absolute temperature, emissivity of the gas and surfaces, surface area and geometrical view factor.", base["Body"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(1.45 * cm, 0.78 * cm, "Detailed IC Engine Exam Answers")
        canvas.drawRightString(A4[0] - 1.45 * cm, 0.78 * cm, f"Page {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUT)
