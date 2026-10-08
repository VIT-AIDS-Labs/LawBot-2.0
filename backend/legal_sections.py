# backend/legal_sections.py
"""
Option B: Actual legal provision text for IPC sections used in our dataset.
This provides the real statutory language for each section code.
"""

IPC_SECTIONS = {
    "IPC_124A": {
        "act": "Indian Penal Code",
        "section": "124A",
        "title": "Sedition",
        "legal_text": (
            "Whoever by words, either spoken or written, or by signs, or by visible "
            "representation, or otherwise, brings or attempts to bring into hatred or "
            "contempt, or excites or attempts to excite disaffection towards the "
            "Government established by law in India shall be punished with imprisonment "
            "for life, to which fine may be added, or with imprisonment which may extend "
            "to three years, to which fine may be added, or with fine."
        ),
    },
    "IPC_124B": {
        "act": "Indian Penal Code",
        "section": "124B",
        "title": "Sedition (Continued Provisions)",
        "legal_text": (
            "Provisions supplementary to Section 124A relating to acts of sedition "
            "and disaffection towards the Government established by law."
        ),
    },
    "IPC_302": {
        "act": "Indian Penal Code",
        "section": "302",
        "title": "Punishment for Murder",
        "legal_text": (
            "Whoever commits murder shall be punished with death, or imprisonment for "
            "life, and shall also be liable to fine."
        ),
    },
    "IPC_304": {
        "act": "Indian Penal Code",
        "section": "304",
        "title": "Punishment for Culpable Homicide not amounting to Murder",
        "legal_text": (
            "Whoever commits culpable homicide not amounting to murder shall be punished "
            "with imprisonment for life, or imprisonment of either description for a term "
            "which may extend to ten years, and shall also be liable to fine, if the act "
            "by which the death is caused is done with the intention of causing death, or "
            "of causing such bodily injury as is likely to cause death; or with imprisonment "
            "of either description for a term which may extend to ten years, or with fine, "
            "or with both, if the act is done with the knowledge that it is likely to cause "
            "death, but without any intention to cause death, or to cause such bodily injury "
            "as is likely to cause death."
        ),
    },
    "IPC_304A": {
        "act": "Indian Penal Code",
        "section": "304A",
        "title": "Causing Death by Negligence",
        "legal_text": (
            "Whoever causes the death of any person by doing any rash or negligent act not "
            "amounting to culpable homicide shall be punished with imprisonment of either "
            "description for a term which may extend to two years, or with fine, or with both."
        ),
    },
    "IPC_307": {
        "act": "Indian Penal Code",
        "section": "307",
        "title": "Attempt to Murder",
        "legal_text": (
            "Whoever does any act with such intention or knowledge, and under such "
            "circumstances that, if he by that act caused death, he would be guilty of "
            "murder, shall be punished with imprisonment of either description for a term "
            "which may extend to ten years, and shall also be liable to fine; and if hurt "
            "is caused to any person by such act, the offender shall be liable either to "
            "imprisonment for life, or to such punishment as is hereinbefore mentioned."
        ),
    },
    "IPC_308": {
        "act": "Indian Penal Code",
        "section": "308",
        "title": "Attempt to commit Culpable Homicide",
        "legal_text": (
            "Whoever does any act with such intention or knowledge and under such "
            "circumstances that, if he by that act caused death, he would be guilty of "
            "culpable homicide not amounting to murder, shall be punished with imprisonment "
            "of either description for a term which may extend to three years, or with fine, "
            "or with both; and if hurt is caused to any person by such act, shall be punished "
            "with imprisonment of either description for a term which may extend to seven "
            "years, or with fine, or with both."
        ),
    },
    "IPC_315": {
        "act": "Indian Penal Code",
        "section": "315",
        "title": "Act done with intent to prevent child being born alive or to cause it to die after birth",
        "legal_text": (
            "Whoever before the birth of any child does any act with the intention of "
            "thereby preventing that child from being born alive or causing it to die after "
            "its birth, and does by such act prevent that child from being born alive, or "
            "causes it to die after its birth, shall, if such act be not caused in good "
            "faith for the purpose of saving the life of the mother, be punished with "
            "imprisonment of either description for a term which may extend to ten years, "
            "or with fine, or with both."
        ),
    },
    "IPC_316": {
        "act": "Indian Penal Code",
        "section": "316",
        "title": "Causing Death of Quick Unborn Child by act amounting to Culpable Homicide",
        "legal_text": (
            "Whoever does any act under such circumstances, that if he thereby caused death "
            "he would be guilty of culpable homicide, and does by such act cause the death "
            "of a quick unborn child, shall be punished with imprisonment of either "
            "description for a term which may extend to ten years, and shall also be liable "
            "to fine."
        ),
    },
    "IPC_323": {
        "act": "Indian Penal Code",
        "section": "323",
        "title": "Punishment for Voluntarily Causing Hurt",
        "legal_text": (
            "Whoever, except in the case provided for by section 334, voluntarily causes "
            "hurt, shall be punished with imprisonment of either description for a term "
            "which may extend to one year, or with fine which may extend to one thousand "
            "rupees, or with both."
        ),
    },
    "IPC_324": {
        "act": "Indian Penal Code",
        "section": "324",
        "title": "Voluntarily Causing Hurt by Dangerous Weapons or Means",
        "legal_text": (
            "Whoever, except in the case provided for by section 334, voluntarily causes "
            "hurt by means of any instrument for shooting, stabbing or cutting, or any "
            "instrument which, used as a weapon of offence, is likely to cause death, or by "
            "means of fire or any heated substance, or by means of any poison or any corrosive "
            "substance, or by means of any explosive substance, or by means of any substance "
            "which it is deleterious to the human body to inhale, to swallow, or to receive "
            "into the blood, or by means of any animal, shall be punished with imprisonment "
            "of either description for a term which may extend to three years, or with fine, "
            "or with both."
        ),
    },
    "IPC_325": {
        "act": "Indian Penal Code",
        "section": "325",
        "title": "Punishment for Voluntarily Causing Grievous Hurt",
        "legal_text": (
            "Whoever, except in the case provided for by section 335, voluntarily causes "
            "grievous hurt, shall be punished with imprisonment of either description for "
            "a term which may extend to seven years, and shall also be liable to fine."
        ),
    },
    "IPC_326": {
        "act": "Indian Penal Code",
        "section": "326",
        "title": "Voluntarily Causing Grievous Hurt by Dangerous Weapons or Means",
        "legal_text": (
            "Whoever, except in the case provided for by section 335, voluntarily causes "
            "grievous hurt by means of any instrument for shooting, stabbing or cutting, or "
            "any instrument which, used as a weapon of offence, is likely to cause death, or "
            "by means of fire or any heated substance, or by means of any poison or any "
            "corrosive substance, or by means of any explosive substance, or by means of any "
            "substance which it is deleterious to the human body to inhale, to swallow, or to "
            "receive into the blood, or by means of any animal, shall be punished with "
            "imprisonment for life, or with imprisonment of either description for a term "
            "which may extend to ten years, and shall also be liable to fine."
        ),
    },
    "IP_326": {
        "act": "Indian Penal Code",
        "section": "326",
        "title": "Voluntarily Causing Grievous Hurt by Dangerous Weapons or Means",
        "legal_text": (
            "Whoever, except in the case provided for by section 335, voluntarily causes "
            "grievous hurt by means of any instrument for shooting, stabbing or cutting, or "
            "any instrument which, used as a weapon of offence, is likely to cause death, "
            "shall be punished with imprisonment for life, or with imprisonment of either "
            "description for a term which may extend to ten years, and shall also be liable "
            "to fine."
        ),
    },
    "IPC_336": {
        "act": "Indian Penal Code",
        "section": "336",
        "title": "Act Endangering Life or Personal Safety of Others",
        "legal_text": (
            "Whoever does any act so rashly or negligently as to endanger human life or the "
            "personal safety of others, shall be punished with imprisonment of either "
            "description for a term which may extend to three months, or with fine which may "
            "extend to two hundred and fifty rupees, or with both."
        ),
    },
    "IPC_339": {
        "act": "Indian Penal Code",
        "section": "339",
        "title": "Wrongful Restraint",
        "legal_text": (
            "Whoever voluntarily obstructs any person so as to prevent that person from "
            "proceeding in any direction in which that person has a right to proceed, is "
            "said to wrongfully restrain that person."
        ),
    },
    "IPC_340": {
        "act": "Indian Penal Code",
        "section": "340",
        "title": "Wrongful Confinement",
        "legal_text": (
            "Whoever wrongfully restrains any person in such a manner as to prevent that "
            "person from proceeding beyond certain circumscribing limits, is said wrongfully "
            "to confine that person."
        ),
    },
    "IPC_341": {
        "act": "Indian Penal Code",
        "section": "341",
        "title": "Punishment for Wrongful Restraint",
        "legal_text": (
            "Whoever wrongfully restrains any person shall be punished with simple "
            "imprisonment for a term which may extend to one month, or with fine which may "
            "extend to five hundred rupees, or with both."
        ),
    },
    "IPC_354": {
        "act": "Indian Penal Code",
        "section": "354",
        "title": "Assault or Criminal Force to Woman with intent to Outrage her Modesty",
        "legal_text": (
            "Whoever assaults or uses criminal force to any woman, intending to outrage or "
            "knowing it to be likely that he will thereby outrage her modesty, shall be "
            "punished with imprisonment of either description for a term which shall not be "
            "less than one year but which may extend to five years, and shall also be liable "
            "to fine."
        ),
    },
    "IPC_354A": {
        "act": "Indian Penal Code",
        "section": "354A",
        "title": "Sexual Harassment and Punishment for Sexual Harassment",
        "legal_text": (
            "A man committing any of the following acts: (i) physical contact and advances "
            "involving unwelcome and explicit sexual overtures; or (ii) a demand or request "
            "for sexual favours; or (iii) showing pornography against the will of a woman; "
            "or (iv) making sexually coloured remarks, shall be guilty of the offence of "
            "sexual harassment. Any man who commits the offence specified in clause (i) or "
            "clause (ii) shall be punished with rigorous imprisonment for a term which may "
            "extend to three years, or with fine, or with both."
        ),
    },
    "IPC_354B": {
        "act": "Indian Penal Code",
        "section": "354B",
        "title": "Assault or Use of Criminal Force to Woman with intent to Disrobe",
        "legal_text": (
            "Any man who assaults or uses criminal force to any woman or abets such act with "
            "the intention of disrobing or compelling her to be naked, shall be punished with "
            "imprisonment of either description for a term which shall not be less than three "
            "years but which may extend to seven years, and shall also be liable to fine."
        ),
    },
    "IPC_363": {
        "act": "Indian Penal Code",
        "section": "363",
        "title": "Punishment for Kidnapping",
        "legal_text": (
            "Whoever kidnaps any person from India or from lawful guardianship, shall be "
            "punished with imprisonment of either description for a term which may extend "
            "to seven years, and shall also be liable to fine."
        ),
    },
    "IPC_363A": {
        "act": "Indian Penal Code",
        "section": "363A",
        "title": "Kidnapping or Maiming a Minor for Purposes of Begging",
        "legal_text": (
            "Whoever kidnaps any minor or, not being the lawful guardian of a minor, obtains "
            "the custody of the minor, in order that such minor may be employed or used for "
            "the purpose of begging shall be punishable with imprisonment of either "
            "description for a term which may extend to ten years, and shall also be liable "
            "to fine."
        ),
    },
    "IPC_366": {
        "act": "Indian Penal Code",
        "section": "366",
        "title": "Kidnapping, Abducting or Inducing Woman to Compel her Marriage",
        "legal_text": (
            "Whoever kidnaps or abducts any woman with intent that she may be compelled, or "
            "knowing it to be likely that she will be compelled, to marry any person against "
            "her will, or in order that she may be forced or seduced to illicit intercourse, "
            "shall be punished with imprisonment of either description for a term which may "
            "extend to ten years, and shall also be liable to fine."
        ),
    },
    "IPC_366A": {
        "act": "Indian Penal Code",
        "section": "366A",
        "title": "Procuration of Minor Girl",
        "legal_text": (
            "Whoever, by any means whatsoever, induces any minor girl under the age of "
            "eighteen years to go from any place or to do any act with intent that such girl "
            "may be, or knowing that it is likely that she will be, forced or seduced to "
            "illicit intercourse with another person shall be punishable with imprisonment "
            "which may extend to ten years, and shall also be liable to fine."
        ),
    },
    "IPC_366B": {
        "act": "Indian Penal Code",
        "section": "366B",
        "title": "Importation of Girl from Foreign Country",
        "legal_text": (
            "Whoever imports into India from any country outside India any girl under the age "
            "of twenty-one years with intent that she may be, or knowing it to be likely that "
            "she will be, forced or seduced to illicit intercourse with another person, shall "
            "be punishable with imprisonment which may extend to ten years and shall also be "
            "liable to fine."
        ),
    },
    "IPC_370": {
        "act": "Indian Penal Code",
        "section": "370",
        "title": "Trafficking of Person",
        "legal_text": (
            "Whoever, for the purpose of exploitation, (a) recruits, (b) transports, "
            "(c) harbours, (d) transfers, or (e) receives, a person or persons, by using "
            "threats, or using force or any other form of coercion, or by abduction, or by "
            "practising fraud or deception, or by abuse of power, or by inducement, shall be "
            "guilty of the offence of trafficking. Whoever commits the offence of trafficking "
            "shall be punished with rigorous imprisonment for a term which shall not be less "
            "than seven years, but which may extend to ten years, and shall also be liable "
            "to fine."
        ),
    },
    "IPC_372": {
        "act": "Indian Penal Code",
        "section": "372",
        "title": "Selling Minor for Purposes of Prostitution",
        "legal_text": (
            "Whoever sells, lets to hire, or otherwise disposes of any person under the age "
            "of eighteen years with intent that such person shall at any age be employed or "
            "used for the purpose of prostitution or illicit intercourse with any person or "
            "for any unlawful and immoral purpose, shall be punished with imprisonment of "
            "either description for a term which may extend to ten years, and shall also be "
            "liable to fine."
        ),
    },
    "IPC_373": {
        "act": "Indian Penal Code",
        "section": "373",
        "title": "Buying Minor for Purposes of Prostitution",
        "legal_text": (
            "Whoever buys, hires or otherwise obtains possession of any person under the age "
            "of eighteen years with intent that such person shall at any age be employed or "
            "used for the purpose of prostitution or illicit intercourse with any person or "
            "for any unlawful and immoral purpose, shall be punished with imprisonment of "
            "either description for a term which may extend to ten years, and shall also be "
            "liable to fine."
        ),
    },
    "IPC_379": {
        "act": "Indian Penal Code",
        "section": "379",
        "title": "Punishment for Theft",
        "legal_text": (
            "Whoever commits theft shall be punished with imprisonment of either description "
            "for a term which may extend to three years, or with fine, or with both."
        ),
    },
    "IPC_380": {
        "act": "Indian Penal Code",
        "section": "380",
        "title": "Theft in Dwelling House",
        "legal_text": (
            "Whoever commits theft in any building, tent or vessel, which building, tent or "
            "vessel is used as a human dwelling, or used for the custody of property, shall "
            "be punished with imprisonment of either description for a term which may extend "
            "to seven years, and shall also be liable to fine."
        ),
    },
    "IPC_390": {
        "act": "Indian Penal Code",
        "section": "390",
        "title": "Robbery",
        "legal_text": (
            "In all robbery there is either theft or extortion. When theft is robbery: Theft "
            "is robbery if, in order to the committing of the theft, or in committing the "
            "theft, or in carrying away or attempting to carry away property obtained by the "
            "theft, the offender, for that end, voluntarily causes or attempts to cause to "
            "any person death or hurt or wrongful restraint, or fear of instant death or of "
            "instant hurt, or of instant wrongful restraint."
        ),
    },
    "IPC_395": {
        "act": "Indian Penal Code",
        "section": "395",
        "title": "Punishment for Dacoity",
        "legal_text": (
            "Whoever commits dacoity shall be punished with imprisonment for life, or with "
            "rigorous imprisonment for a term which may extend to ten years, and shall also "
            "be liable to fine."
        ),
    },
    "IPC_403": {
        "act": "Indian Penal Code",
        "section": "403",
        "title": "Dishonest Misappropriation of Property",
        "legal_text": (
            "Whoever dishonestly misappropriates or converts to his own use any movable "
            "property, shall be punished with imprisonment of either description for a term "
            "which may extend to two years, or with fine, or with both."
        ),
    },
    "IPC_404": {
        "act": "Indian Penal Code",
        "section": "404",
        "title": "Dishonest Misappropriation of Property possessed by Deceased Person",
        "legal_text": (
            "Whoever dishonestly misappropriates or converts to his own use property, knowing "
            "that such property was in the possession of a deceased person at the time of that "
            "person's death, and has not since been in the possession of any person legally "
            "entitled to such possession, shall be punished with imprisonment of either "
            "description for a term which may extend to three years, and shall also be liable "
            "to fine."
        ),
    },
    "IPC_406": {
        "act": "Indian Penal Code",
        "section": "406",
        "title": "Punishment for Criminal Breach of Trust",
        "legal_text": (
            "Whoever commits criminal breach of trust shall be punished with imprisonment of "
            "either description for a term which may extend to three years, or with fine, or "
            "with both."
        ),
    },
    "IPC_409": {
        "act": "Indian Penal Code",
        "section": "409",
        "title": "Criminal Breach of Trust by Public Servant, Banker, Merchant or Agent",
        "legal_text": (
            "Whoever, being in any manner entrusted with property, or with any dominion over "
            "property in his capacity of a public servant or in the way of his business as a "
            "banker, merchant, factor, broker, attorney or agent, commits criminal breach of "
            "trust in respect of that property, shall be punished with imprisonment for life, "
            "or with imprisonment of either description for a term which may extend to ten "
            "years, and shall also be liable to fine."
        ),
    },
    "IPC_411": {
        "act": "Indian Penal Code",
        "section": "411",
        "title": "Dishonestly Receiving Stolen Property",
        "legal_text": (
            "Whoever dishonestly receives or retains any stolen property, knowing or having "
            "reason to believe the same to be stolen property, shall be punished with "
            "imprisonment of either description for a term which may extend to three years, "
            "or with fine, or with both."
        ),
    },
    "IPC_415": {
        "act": "Indian Penal Code",
        "section": "415",
        "title": "Cheating",
        "legal_text": (
            "Whoever, by deceiving any person, fraudulently or dishonestly induces the person "
            "so deceived to deliver any property to any person, or to consent that any person "
            "shall retain any property, or intentionally induces the person so deceived to do "
            "or omit to do anything which he would not do or omit if he were not so deceived, "
            "and which act or omission causes or is likely to cause damage or harm to that "
            "person in body, mind, reputation or property, is said to cheat."
        ),
    },
    "IPC_420": {
        "act": "Indian Penal Code",
        "section": "420",
        "title": "Cheating and Dishonestly Inducing Delivery of Property",
        "legal_text": (
            "Whoever cheats and thereby dishonestly induces the person deceived to deliver any "
            "property to any person, or to make, alter or destroy the whole or any part of a "
            "valuable security, or anything which is signed or sealed, and which is capable of "
            "being converted into a valuable security, shall be punished with imprisonment of "
            "either description for a term which may extend to seven years, and shall also be "
            "liable to fine."
        ),
    },
    "IPC_426": {
        "act": "Indian Penal Code",
        "section": "426",
        "title": "Punishment for Mischief",
        "legal_text": (
            "Whoever commits mischief shall be punished with imprisonment of either description "
            "for a term which may extend to three months, or with fine, or with both."
        ),
    },
    "IPC_447": {
        "act": "Indian Penal Code",
        "section": "447",
        "title": "Punishment for Criminal Trespass",
        "legal_text": (
            "Whoever commits criminal trespass shall be punished with imprisonment of either "
            "description for a term which may extend to three months, or with fine which may "
            "extend to five hundred rupees, or with both."
        ),
    },
    "IPC_498A": {
        "act": "Indian Penal Code",
        "section": "498A",
        "title": "Husband or Relative of Husband Subjecting Woman to Cruelty",
        "legal_text": (
            "Whoever, being the husband or the relative of the husband of a woman, subjects "
            "such woman to cruelty shall be punished with imprisonment for a term which may "
            "extend to three years and shall also be liable to fine. For the purposes of this "
            "section, cruelty means any wilful conduct which is of such a nature as is likely "
            "to drive the woman to commit suicide or to cause grave injury or danger to life, "
            "limb or health of the woman; or harassment of the woman where such harassment is "
            "with a view to coercing her or any person related to her to meet any unlawful "
            "demand for any property or valuable security or is on account of failure by her "
            "or any person related to her to meet such demand."
        ),
    },
    "IPC_505": {
        "act": "Indian Penal Code",
        "section": "505",
        "title": "Statements Conducing to Public Mischief",
        "legal_text": (
            "Whoever makes, publishes or circulates any statement, rumour or report, with "
            "intent to cause, or which is likely to cause, fear or alarm to the public, or to "
            "any section of the public whereby any person may be induced to commit an offence "
            "against the State or against the public tranquility, shall be punished with "
            "imprisonment which may extend to three years, or with fine, or with both."
        ),
    },
    "IPC_506": {
        "act": "Indian Penal Code",
        "section": "506",
        "title": "Punishment for Criminal Intimidation",
        "legal_text": (
            "Whoever commits the offence of criminal intimidation shall be punished with "
            "imprisonment of either description for a term which may extend to two years, or "
            "with fine, or with both; if threat be to cause death or grievous hurt, etc., "
            "shall be punished with imprisonment of either description for a term which may "
            "extend to seven years, or with fine, or with both."
        ),
    },
    "IPC_509": {
        "act": "Indian Penal Code",
        "section": "509",
        "title": "Word, Gesture or Act intended to Insult the Modesty of a Woman",
        "legal_text": (
            "Whoever, intending to insult the modesty of any woman, utters any word, makes "
            "any sound or gesture, or exhibits any object, intending that such word or sound "
            "shall be heard, or that such gesture or object shall be seen, by such woman, or "
            "intrudes upon the privacy of such woman, shall be punished with simple imprisonment "
            "for a term which may extend to three years, and also with fine."
        ),
    },
}


def get_section_info(section_code: str) -> dict | None:
    """
    Look up full legal information for a section code.
    Returns dict with act, section, title, legal_text or None.
    """
    # Direct lookup
    if section_code in IPC_SECTIONS:
        return IPC_SECTIONS[section_code]

    # Try normalizing: strip whitespace, uppercase
    normalized = section_code.strip().upper().replace(" ", "_")
    if normalized in IPC_SECTIONS:
        return IPC_SECTIONS[normalized]

    # Try to parse section code pattern and extract info
    # e.g., "IPC_304" -> act="Indian Penal Code", section="304"
    if normalized.startswith("IPC_") or normalized.startswith("IP_"):
        prefix = "IPC_" if normalized.startswith("IPC_") else "IP_"
        section_num = normalized[len(prefix):]
        return {
            "act": "Indian Penal Code",
            "section": section_num,
            "title": f"Section {section_num}",
            "legal_text": None,  # Not in our lookup
        }

    return None


def get_all_section_codes() -> list[str]:
    """Return all known section codes."""
    return list(IPC_SECTIONS.keys())
