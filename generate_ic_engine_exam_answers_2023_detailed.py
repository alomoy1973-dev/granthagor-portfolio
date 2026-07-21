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


OUT = "IC_Engine_Exam_Answers_2023_Detailed.pdf"


def p(text, style):
    return Paragraph(text, style)


def add_bullets(story, items, style):
    for item in items:
        story.append(Paragraph(item, style, bulletText="-"))


def add_question(story, text, styles):
    story.append(Paragraph(text, styles["Question"]))


def math_box(lines, code_style):
    return KeepTogether([Preformatted("\n".join(lines), code_style), Spacer(1, 4)])


def make_table(rows, widths):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.35),
        ("LEADING", (0, 0), (-1, -1), 10.5),
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
        OUT,
        pagesize=A4,
        leftMargin=1.45 * cm,
        rightMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.35 * cm,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER,
        fontName="Helvetica-Bold", fontSize=16.3, leading=20,
        textColor=colors.HexColor("#172554"), spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="SubCenter", parent=styles["Normal"], alignment=TA_CENTER,
        fontSize=9.2, leading=11.7, textColor=colors.HexColor("#374151"),
        spaceAfter=13,
    ))
    styles.add(ParagraphStyle(
        name="Part", parent=styles["Heading1"], alignment=TA_CENTER,
        fontName="Helvetica-Bold", fontSize=13.2, leading=16,
        textColor=colors.white, backColor=colors.HexColor("#1d4ed8"),
        borderPadding=(5, 4, 5, 4), spaceBefore=8, spaceAfter=9,
    ))
    styles.add(ParagraphStyle(
        name="Question", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=10.55, leading=13.4, textColor=colors.HexColor("#111827"),
        spaceBefore=9, spaceAfter=4, keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="Body", parent=styles["BodyText"], alignment=TA_LEFT,
        fontName="Helvetica", fontSize=9.25, leading=12.2, spaceAfter=4.2,
    ))
    styles.add(ParagraphStyle(
        name="ExamBullet", parent=styles["BodyText"], leftIndent=14,
        firstLineIndent=0, bulletIndent=5, fontName="Helvetica",
        fontSize=9.05, leading=11.8, spaceAfter=2.5,
    ))
    styles.add(ParagraphStyle(
        name="SubHead", parent=styles["Heading3"], fontName="Helvetica-Bold",
        fontSize=9.65, leading=12, textColor=colors.HexColor("#1f2937"),
        spaceBefore=5, spaceAfter=3,
    ))
    code = ParagraphStyle(
        "MathBox", parent=styles["Code"], fontName="Courier", fontSize=8.25,
        leading=10.6, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=5,
        borderWidth=0.45, borderColor=colors.HexColor("#bfdbfe"),
        borderPadding=6, backColor=colors.HexColor("#f8fbff"),
    )

    story = []
    story.append(p("Internal Combustion Engine: Detailed Exam Answers", styles["TitleCenter"]))
    story.append(p("Course: MEE 401 | B.Sc. Mechanical Engineering Examination 2023 question page", styles["SubCenter"]))
    story.append(p("PART-A", styles["Part"]))

    add_question(story, "1(a) Differentiate between engine and machine. Classify different types of heat engine and briefly explain their working principle.", styles)
    story.append(p("<b>Difference between engine and machine:</b> A machine is a device or combination of mechanisms used to transmit or transform motion and force for doing useful work. An engine is a special type of machine which converts some form of energy, usually heat energy, into mechanical work. Thus every engine is a machine, but every machine is not an engine.", styles["Body"]))
    story.append(make_table([
        ["Basis", "Engine", "Machine"],
        ["Main function", "Converts energy into mechanical work.", "Transmits, modifies or utilizes mechanical work."],
        ["Energy conversion", "Primary energy conversion device.", "May not convert energy; often only changes motion/force."],
        ["Example", "Petrol engine, diesel engine, gas turbine.", "Lathe, pump, crane, gear train."],
        ["Output", "Produces power.", "Uses or transmits power for a task."],
    ], [3.6 * cm, 6.2 * cm, 6.2 * cm]))
    story.append(Spacer(1, 5))
    story.append(p("<b>Classification of heat engines:</b> Heat engines convert heat energy into mechanical work. They are mainly classified into external combustion engines and internal combustion engines.", styles["Body"]))
    add_bullets(story, [
        "<b>External combustion engine:</b> Combustion of fuel takes place outside the working cylinder. Heat is transferred to a working fluid such as steam, which then expands and produces work. Examples are steam engine and steam turbine.",
        "<b>Internal combustion engine:</b> Fuel burns inside the engine cylinder or combustion chamber. The high-pressure combustion gases directly act on the piston or turbine blades. Examples are petrol engine, diesel engine and gas turbine.",
        "<b>Reciprocating heat engine:</b> The working fluid acts on a piston moving to and fro inside a cylinder. Petrol and diesel engines are common examples.",
        "<b>Rotary heat engine:</b> The working fluid produces rotary motion directly. Gas turbines and Wankel engines are examples.",
    ], styles["ExamBullet"])
    story.append(p("<b>Working principle:</b> In a heat engine, fuel is burnt and heat is released. The working fluid receives this heat, its pressure and temperature rise, and it expands to produce mechanical work. A part of the supplied heat is converted into useful work and the remaining part is rejected to the surroundings, according to the second law of thermodynamics.", styles["Body"]))

    add_question(story, "1(b) Describe different engine components of an IC engine with proper sketch.", styles)
    story.append(p("An IC engine consists of several fixed and moving parts. These parts work together to admit charge, compress it, burn the fuel, produce power and discharge exhaust gases.", styles["Body"]))
    story.append(math_box([
        "Simple line sketch of a reciprocating IC engine:",
        "",
        "          Spark plug / Injector",
        "                 |",
        "        _________|_________    Cylinder head",
        "       |   Inlet / Exhaust |",
        "       |      valves       |",
        "       |-------------------|",
        "       |      Piston       |    Cylinder block",
        "       |___________________|",
        "              |",
        "        Connecting rod",
        "              |",
        "          Crankshaft  ---- Flywheel",
        "       Crankcase and oil sump below",
    ], code))
    add_bullets(story, [
        "<b>Cylinder block:</b> It contains the cylinder in which the piston reciprocates. It also supports water jackets, crankcase and other parts.",
        "<b>Cylinder head:</b> It closes the top of the cylinder and carries inlet valve, exhaust valve, spark plug or injector.",
        "<b>Piston:</b> It receives gas pressure and transmits force to the connecting rod. It also helps seal the combustion chamber.",
        "<b>Piston rings:</b> Compression rings prevent leakage of gases, while oil rings control lubricating oil on the cylinder wall.",
        "<b>Connecting rod:</b> It connects the piston with the crankshaft and transmits force from piston to crank.",
        "<b>Crankshaft:</b> It converts reciprocating motion of the piston into rotary motion.",
        "<b>Crankcase:</b> It supports the crankshaft and forms a housing for lubricating oil.",
        "<b>Valves and valve gear:</b> Inlet and exhaust valves control the admission of fresh charge and discharge of burnt gases.",
        "<b>Camshaft:</b> It operates the valves at correct timing through tappets, push rods and rocker arms.",
        "<b>Flywheel:</b> It stores energy during power stroke and supplies energy during other strokes to reduce speed fluctuation.",
        "<b>Carburetor/fuel injector:</b> The carburetor prepares air-fuel mixture in old SI engines; the injector supplies fuel in atomized form.",
        "<b>Spark plug or injector:</b> Spark plug ignites mixture in SI engines; injector introduces diesel fuel into CI engines.",
    ], styles["ExamBullet"])

    add_question(story, "2(a) Find out air-standard efficiency of Otto cycle. Prove that higher compression ratio is the most effective way of improving the performance of a constant-volume cycle engine.", styles)
    story.append(p("The Otto cycle is the ideal cycle for a spark ignition engine. It consists of isentropic compression, constant-volume heat addition, isentropic expansion and constant-volume heat rejection.", styles["Body"]))
    story.append(math_box([
        "Otto cycle processes:",
        "  1-2: Isentropic compression",
        "  2-3: Constant-volume heat addition",
        "  3-4: Isentropic expansion",
        "  4-1: Constant-volume heat rejection",
        "",
        "Heat supplied:  Qs = cv(T3 - T2)",
        "Heat rejected:  Qr = cv(T4 - T1)",
        "",
        "Efficiency:",
        "  eta = 1 - Qr/Qs",
        "      = 1 - [cv(T4 - T1)]/[cv(T3 - T2)]",
        "      = 1 - (T4 - T1)/(T3 - T2)",
    ], code))
    story.append(math_box([
        "For isentropic compression and expansion:",
        "  T2/T1 = r^(k-1)",
        "  T3/T4 = r^(k-1)",
        "",
        "Therefore:",
        "  T2 = T1 r^(k-1)  and  T3 = T4 r^(k-1)",
        "",
        "Substituting in the efficiency expression gives:",
        "             1",
        "  eta = 1 - ---------",
        "          r^(k-1)",
        "",
        "where r = compression ratio and k = cp/cv.",
    ], code))
    story.append(p("From the expression <b>eta = 1 - 1/r^(k-1)</b>, it is clear that Otto-cycle efficiency depends mainly on compression ratio and the value of k. For a given working fluid, k is almost fixed; therefore increasing the compression ratio is the most direct and effective method of improving the thermal efficiency of a constant-volume cycle engine. Higher compression ratio raises the temperature and pressure before combustion, increases expansion work and reduces the fraction of heat rejected.", styles["Body"]))
    story.append(p("However, in a practical SI engine the compression ratio cannot be increased indefinitely because knocking may occur. Therefore high-octane fuel and proper combustion chamber design are required when high compression ratio is used.", styles["Body"]))

    add_question(story, "2(b) A petrol engine uses fuel of calorific value 42000 kJ/kg. Pressures at 5% and 75% of the compression stroke are 1.2 bar and 4.8 bar respectively. Compression follows pV^1.3 = constant. Find compression ratio and specific fuel consumption if relative efficiency compared with air-standard efficiency is 60%.", styles)
    story.append(p("The piston is assumed to move from BDC to TDC during compression. At 5% of the compression stroke, 95% of the swept volume is still above the piston. At 75% of the compression stroke, 25% of the swept volume is still above the piston.", styles["Body"]))
    story.append(math_box([
        "Given:",
        "  Calorific value, CV = 42000 kJ/kg",
        "  Pressure at 5% compression stroke, p5 = 1.2 bar",
        "  Pressure at 75% compression stroke, p75 = 4.8 bar",
        "  Compression law: pV^1.3 = constant",
        "  Relative efficiency = 60% = 0.60",
    ], code))
    story.append(math_box([
        "Let:",
        "  Vs = swept volume",
        "  Vc = clearance volume",
        "  r  = compression ratio = (Vs + Vc)/Vc",
        "",
        "At 5% of compression stroke:",
        "  V5 = Vc + 0.95Vs",
        "     = Vc + 0.95(r - 1)Vc",
        "     = Vc(0.05 + 0.95r)",
        "",
        "At 75% of compression stroke:",
        "  V75 = Vc + 0.25Vs",
        "      = Vc + 0.25(r - 1)Vc",
        "      = Vc(0.75 + 0.25r)",
    ], code))
    story.append(math_box([
        "Using pV^1.3 = constant:",
        "  p5(V5)^1.3 = p75(V75)^1.3",
        "",
        "  V5/V75 = (p75/p5)^(1/1.3)",
        "          = (4.8/1.2)^(1/1.3)",
        "          = 4^(1/1.3)",
        "          = 2.9048",
        "",
        "Therefore:",
        "  (0.05 + 0.95r)/(0.75 + 0.25r) = 2.9048",
        "",
        "  0.05 + 0.95r = 2.9048(0.75 + 0.25r)",
        "  0.05 + 0.95r = 2.1786 + 0.7262r",
        "  0.2238r = 2.1286",
        "",
        "  r = 9.51",
    ], code))
    story.append(math_box([
        "Air-standard Otto efficiency, taking k = 1.4:",
        "             1",
        "  eta_as = 1 - ---------",
        "           r^(k-1)",
        "",
        "         = 1 - 1/(9.51)^0.4",
        "         = 0.5938",
        "         = 59.38%",
        "",
        "Actual thermal efficiency:",
        "  eta_actual = relative efficiency x air-standard efficiency",
        "             = 0.60 x 0.5938",
        "             = 0.3563 = 35.63%",
    ], code))
    story.append(math_box([
        "Specific fuel consumption:",
        "  Brake thermal efficiency = output energy / fuel energy",
        "",
        "  For 1 kWh output, useful energy = 3600 kJ",
        "",
        "  sfc = 3600/(eta_actual x CV)",
        "      = 3600/(0.3563 x 42000)",
        "      = 0.2406 kg/kWh",
    ], code))
    story.append(make_table([
        ["Final result", "Answer"],
        ["Compression ratio", "r = 9.51"],
        ["Air-standard Otto efficiency", "59.38%"],
        ["Actual thermal efficiency", "35.63%"],
        ["Specific fuel consumption", "0.241 kg/kWh"],
    ], [6.3 * cm, 9.5 * cm]))

    add_question(story, "3(a) Classify different types of fossil fuels. Can we use solid fuels in IC engines? Justify your answer.", styles)
    story.append(p("Fossil fuels are naturally occurring fuels formed from buried organic matter over millions of years under heat and pressure. They contain mainly carbon and hydrogen and release heat during combustion.", styles["Body"]))
    add_bullets(story, [
        "<b>Solid fossil fuels:</b> peat, lignite, bituminous coal and anthracite. They are mainly used in boilers, furnaces and power plants.",
        "<b>Liquid fossil fuels:</b> crude petroleum and its products such as petrol, diesel, kerosene, furnace oil and lubricating oil.",
        "<b>Gaseous fossil fuels:</b> natural gas, coal gas, producer gas and refinery gas.",
    ], styles["ExamBullet"])
    story.append(p("<b>Use of solid fuels in IC engines:</b> Solid fuels are not suitable for direct use in ordinary IC engines. The fuel in an IC engine must be supplied quickly, metered accurately, mixed properly with air and burnt within a very short time. Solid fuel cannot be atomized like petrol or diesel, and its combustion is too slow for high-speed cylinder operation.", styles["Body"]))
    add_bullets(story, [
        "Ash and dust from solid fuel cause abrasion, deposits and valve/cylinder wear.",
        "Feeding solid fuel into a closed cylinder at high speed is mechanically difficult.",
        "Load control, starting and speed control become poor.",
        "Incomplete combustion produces smoke, carbon deposits and low efficiency.",
        "Solid fuels may be converted into gaseous fuel, such as producer gas, and then used in gas engines.",
    ], styles["ExamBullet"])

    add_question(story, "3(b) Briefly explain refining process of petroleum. What is producer gas?", styles)
    story.append(p("<b>Petroleum refining:</b> Crude petroleum is a complex mixture of hydrocarbons. Refining separates crude oil into useful fractions and improves their quality for practical use.", styles["Body"]))
    add_bullets(story, [
        "<b>Pre-treatment:</b> Water, salts and solid impurities are removed from crude oil to reduce corrosion and fouling.",
        "<b>Fractional distillation:</b> Crude oil is heated and sent to a fractionating column. Components separate according to boiling range. Light gases leave at the top, followed by petrol, naphtha, kerosene, diesel, lubricating oil and heavy residue.",
        "<b>Cracking:</b> Heavy hydrocarbons are broken into lighter products such as petrol and diesel by thermal or catalytic cracking.",
        "<b>Reforming:</b> Low-octane hydrocarbons are converted into high-octane compounds to improve petrol quality.",
        "<b>Treating and blending:</b> Sulphur, gum and other impurities are removed. Different fractions and additives are blended to meet fuel specifications.",
    ], styles["ExamBullet"])
    story.append(p("<b>Producer gas:</b> Producer gas is a low-calorific gaseous fuel obtained by passing air, or air and steam, through a bed of red-hot coke or coal. It contains mainly carbon monoxide, nitrogen, hydrogen, carbon dioxide and small amounts of methane. Because it contains much nitrogen, its calorific value is low, but it can be used in gas engines and industrial furnaces.", styles["Body"]))

    add_question(story, "4(a) Briefly explain different characteristics of SI engines.", styles)
    add_bullets(story, [
        "SI means spark ignition. The air-fuel mixture is ignited by an electric spark from a spark plug.",
        "The fuel is usually petrol, gasoline, LPG, CNG or alcohol-blended fuel.",
        "A homogeneous air-fuel mixture is generally prepared before combustion, either by carburetor or fuel injection.",
        "The compression ratio is lower than that of CI engines, usually about 6:1 to 12:1, because of knocking limitation.",
        "Combustion is initiated at the spark plug and flame propagates through the mixture.",
        "Speed is generally controlled by throttling the air-fuel mixture.",
        "SI engines are lighter, smoother and suitable for high-speed operation.",
        "They have easier starting and lower noise compared with CI engines.",
        "Thermal efficiency is generally lower than that of diesel engines because of lower compression ratio and throttling losses.",
        "Important requirements are proper ignition timing, correct air-fuel ratio and fuel with sufficient octane rating.",
    ], styles["ExamBullet"])

    add_question(story, "4(b) What is flash point and fire point of any fuel? Why is it important to know these two points? Briefly explain octane rating and cetane rating of fuel.", styles)
    story.append(p("<b>Flash point:</b> Flash point is the lowest temperature at which a fuel gives off enough vapour to form an ignitable mixture with air and produces a momentary flash when an external flame is applied.", styles["Body"]))
    story.append(p("<b>Fire point:</b> Fire point is the lowest temperature at which the vapour of a fuel continues to burn for a short period after ignition. Fire point is always higher than flash point.", styles["Body"]))
    story.append(p("<b>Importance:</b> Flash point and fire point indicate the safety of a fuel during storage, handling and transportation. A fuel with very low flash point is more dangerous because it can form flammable vapour at low temperature. These properties also help select suitable fuels and lubricating oils for engines.", styles["Body"]))
    add_bullets(story, [
        "<b>Octane rating:</b> It measures the anti-knock quality of SI engine fuel. Iso-octane is assigned 100 and normal heptane is assigned 0. A higher octane number means better resistance to knocking.",
        "<b>Cetane rating:</b> It measures the ignition quality of diesel fuel. A higher cetane number means shorter ignition delay and smoother combustion in CI engines. Cetane is assigned 100 in the reference scale.",
    ], styles["ExamBullet"])

    story.append(PageBreak())
    story.append(p("PART-B", styles["Part"]))

    add_question(story, "1(a) Briefly explain the working principle of a simple carburetor.", styles)
    story.append(p("A simple carburetor is used in an SI engine to prepare an air-fuel mixture. It works on the principle of pressure drop in a venturi. When air passes through the venturi throat, its velocity increases and pressure decreases. The pressure in the float chamber is nearly atmospheric, so fuel flows from the float chamber through the fuel jet into the low-pressure region of the venturi.", styles["Body"]))
    add_bullets(story, [
        "The float chamber maintains a constant fuel level.",
        "The venturi creates suction for fuel discharge.",
        "The fuel jet meters the quantity of fuel.",
        "The throttle valve controls the quantity of mixture supplied to the engine.",
        "The choke valve enriches the mixture during cold starting.",
        "The fuel is atomized by the high-speed air stream and then flows to the cylinder as a combustible mixture.",
    ], styles["ExamBullet"])

    add_question(story, "1(b) Why does vapour lock occur in any fuel system? Briefly explain the working principle of a battery ignition system.", styles)
    story.append(p("<b>Vapour lock:</b> Vapour lock occurs when liquid fuel vaporizes in the fuel line, fuel pump or carburetor before reaching the engine. Vapour bubbles restrict the flow of liquid fuel and the engine may misfire, lose power or stop. It is common when fuel temperature is high, fuel has high volatility, fuel lines are close to hot engine parts, or suction pressure in the fuel line is low.", styles["Body"]))
    story.append(p("<b>Battery ignition system:</b> A battery ignition system uses a battery as the source of electrical energy. Current from the battery flows through the ignition switch, primary winding of the ignition coil and contact breaker. When the contact breaker opens, the primary current is suddenly interrupted and a high voltage is induced in the secondary winding of the coil. This high voltage is sent by the distributor to the correct spark plug, where it jumps across the plug gap and ignites the mixture.", styles["Body"]))
    add_bullets(story, [
        "Battery supplies low-voltage current.",
        "Ignition coil steps up the voltage.",
        "Contact breaker makes and breaks the primary circuit.",
        "Condenser reduces sparking at contact points and helps rapid collapse of magnetic field.",
        "Distributor sends high voltage to spark plugs in firing order.",
        "Spark plug produces spark inside the combustion chamber.",
    ], styles["ExamBullet"])

    add_question(story, "2(a) Mention some necessity of engine cooling. Briefly explain gas temperature variation curve for a typical four-stroke SI engine.", styles)
    story.append(p("Only a part of the heat released by combustion is converted into useful work. The remaining heat must be removed from engine parts to keep them within safe temperature limits. Therefore cooling is essential.", styles["Body"]))
    add_bullets(story, [
        "To prevent overheating of cylinder, piston, valves and cylinder head.",
        "To maintain strength of engine parts and avoid distortion.",
        "To protect lubricating oil from burning or losing viscosity.",
        "To reduce knocking tendency in SI engines.",
        "To maintain proper clearance between piston and cylinder.",
        "To improve volumetric efficiency by avoiding excessive heating of incoming charge.",
        "To increase engine reliability and service life.",
    ], styles["ExamBullet"])
    story.append(p("<b>Gas temperature variation:</b> During suction the gas temperature is low because fresh charge enters the cylinder. During compression, temperature rises due to compression. Spark occurs before TDC and combustion continues after TDC, so maximum temperature is reached shortly after TDC. During expansion, gas temperature decreases as work is done on the piston. During exhaust, hot products leave the cylinder and the temperature falls further.", styles["Body"]))
    story.append(math_box([
        "Temperature",
        "   ^                     peak after TDC",
        "   |                        /\\",
        "   |                       /  \\",
        "   |      compression     /    \\ expansion",
        "   |____ suction ________/      \\_____ exhaust",
        "   +--------------------------------------------> crank angle",
    ], code))

    add_question(story, "2(b) How can a valve be cooled? Briefly explain forced circulation liquid cooled system with necessary sketch.", styles)
    story.append(p("<b>Valve cooling:</b> The exhaust valve is cooled mainly by conduction. When the valve rests on its seat, heat flows from the valve head to the valve seat and then to the cylinder head and cooling water. Some heat also flows through the valve stem to the valve guide. Good valve seating, proper material selection and correct clearance are necessary. In heavy-duty engines, hollow sodium-cooled valves may be used.", styles["Body"]))
    story.append(math_box([
        "Forced circulation liquid cooling system:",
        "",
        "       Radiator",
        "   +-------------+",
        "   |             |<----- Hot water from engine",
        "   +-------------+",
        "          | cool water",
        "          v",
        "      Water pump ----> Engine water jacket",
        "          ^                 |",
        "          |                 v",
        "       Thermostat <----- Hot water outlet",
        "          Fan blows air through radiator",
    ], code))
    story.append(p("In a forced circulation liquid cooling system, a water pump circulates coolant through the water jackets around the cylinder and cylinder head. The coolant absorbs heat from engine parts and flows to the radiator. In the radiator, heat is transferred from coolant to air. A fan increases air flow through the radiator. The cooled water then returns to the pump and repeats the cycle. A thermostat controls coolant flow so that the engine quickly reaches and maintains proper operating temperature.", styles["Body"]))

    add_question(story, "3(a) Mention the difference between supercharger and turbocharger. Draw the valve timing diagram of an SI engine.", styles)
    story.append(make_table([
        ["Basis", "Supercharger", "Turbocharger"],
        ["Drive", "Driven mechanically by crankshaft.", "Driven by exhaust gas turbine."],
        ["Energy source", "Consumes part of engine power.", "Uses waste exhaust energy."],
        ["Response", "Immediate boost, almost no lag.", "May have turbo lag at low speed."],
        ["Efficiency", "Power increases but mechanical loss also increases.", "Generally improves engine efficiency and power."],
        ["Construction", "Needs belt, gear or chain drive.", "Needs turbine, compressor and high-temperature exhaust parts."],
        ["Application", "Used where quick response is required.", "Common in modern diesel and petrol engines."],
    ], [3.5 * cm, 6.2 * cm, 6.2 * cm]))
    story.append(Spacer(1, 5))
    story.append(math_box([
        "Typical valve timing diagram of four-stroke SI engine:",
        "",
        "  IVO: Inlet valve opens 10-20 deg before TDC",
        "  IVC: Inlet valve closes 30-45 deg after BDC",
        "  EVO: Exhaust valve opens 35-50 deg before BDC",
        "  EVC: Exhaust valve closes 10-15 deg after TDC",
        "  Spark: 20-35 deg before TDC",
        "",
        "             TDC",
        "              |  overlap",
        "        EVC __|__ IVO",
        "            /     \\",
        "           /       \\",
        "       EVO           IVC",
        "              BDC",
    ], code))

    add_question(story, "3(b) Write down the advantages and disadvantages of two-stroke engines.", styles)
    story.append(p("<b>Advantages:</b>", styles["Body"]))
    add_bullets(story, [
        "One power stroke is obtained in every crankshaft revolution, so power output is high for the same size.",
        "The engine is simple because ports may be used instead of valves.",
        "It is lighter and more compact than a four-stroke engine of equal power.",
        "Initial cost is lower due to fewer parts.",
        "Turning moment is more uniform because power strokes occur more frequently.",
        "It can operate in any orientation in some small-engine applications.",
    ], styles["ExamBullet"])
    story.append(p("<b>Disadvantages:</b>", styles["Body"]))
    add_bullets(story, [
        "Scavenging is not perfect; some fresh charge may escape with exhaust gases.",
        "Fuel consumption is higher than in four-stroke engines.",
        "Thermal efficiency is lower due to short-circuiting and incomplete scavenging.",
        "Lubrication is more difficult, especially in small crankcase-scavenged engines.",
        "Exhaust emissions and smoke are higher.",
        "Engine parts may run hotter and wear faster.",
        "Noise level is generally higher.",
    ], styles["ExamBullet"])

    add_question(story, "4. Write down short note on the following.", styles)
    story.append(p("(a) Ice formation.", styles["SubHead"]))
    story.append(p("Ice formation in a carburetor occurs when the temperature of moist air falls below freezing due to fuel vaporization and pressure drop in the venturi. Ice may form around the throttle valve and venturi, restricting air flow and causing loss of power or engine stoppage. Carburetor heating or warm intake air is used to prevent it.", styles["Body"]))
    story.append(p("(b) Dwell angle.", styles["SubHead"]))
    story.append(p("Dwell angle is the angle through which the distributor cam rotates while the contact breaker points remain closed. During this period current flows through the primary winding of the ignition coil and builds up the magnetic field. Correct dwell angle is necessary for a strong spark. Too small dwell gives weak spark; too large dwell overheats the coil and points.", styles["Body"]))
    story.append(p("(c) LPG and LNG.", styles["SubHead"]))
    story.append(p("LPG means liquefied petroleum gas, mainly propane and butane stored as liquid under moderate pressure. It is used in SI engines because it burns cleanly and has good anti-knock quality. LNG means liquefied natural gas, mainly methane stored at very low temperature. It has high octane quality and low emissions, but requires cryogenic storage.", styles["Body"]))
    story.append(p("(d) Air-standard cycle.", styles["SubHead"]))
    story.append(p("An air-standard cycle is an ideal thermodynamic cycle used to analyze IC engines. Air is assumed to be the working fluid throughout the cycle and behaves as an ideal gas. Combustion is replaced by external heat addition and exhaust is replaced by heat rejection. Otto, Diesel and Dual cycles are common air-standard cycles.", styles["Body"]))
    story.append(p("(e) Ballast resistor.", styles["SubHead"]))
    story.append(p("A ballast resistor is used in the primary circuit of a battery ignition system to limit current through the ignition coil. It protects the coil and contact breaker from overheating during normal operation. During starting, it may be bypassed to provide higher voltage to the coil and produce a stronger spark.", styles["Body"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(1.45 * cm, 0.78 * cm, "Detailed IC Engine Exam Answers - 2023")
        canvas.drawRightString(A4[0] - 1.45 * cm, 0.78 * cm, f"Page {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUT)
