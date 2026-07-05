"""
Optional seed script — populates the database with a few well-documented,
public-record cases so you can see the API working immediately.

Run with:
    python -m app.seed
"""

from database import SessionLocal, engine, Base
import models
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./test.db", echo=True)

Base.metadata.create_all(bind=engine)


SAMPLE_KILLERS = [
    {
        "name": "Theodore Robert Bundy",
        "known_as": ["Ted Bundy"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Ted_Bundy_mugshot.jpg",
        "birth_year": 1946,
        "birth_location": "Burlington, Vermont, USA",
        "murder_count_proved": 3,
        "murder_count_actual": 30,
        "country": "United States",
        "years_active_from": 1974,
        "years_active_to": 1978,
        "active_in_provinces": ["Washington", "Utah", "Colorado", "Florida"],
        "method": "Approached victims using a feigned injury or authority-figure ruse to lower their guard before attacking.",
        "sentence_details": "Convicted on 3 counts of murder (Florida, 1979-80); sentenced to death. Executed by electric chair in Florida on 24 January 1989.",
        "motive": "No single disclosed motive; psychological evaluations pointed to deep-seated antisocial and violent impulses.",
        "additional_info": "Escaped custody twice before final capture. Case significantly influenced FBI criminal profiling methods.",
        "status": "deceased",
        "caught_by": "Traffic stop for a vehicle violation in Florida (1978) led to identification of stolen items linking him to prior crimes.",
        "victim_stats": {
            "female": 3, "male": 0,
            "under 18": 1, "18-30": 2, "31-45": 0, "46-60": 0, "above 60": 0,
            "major_occupation": "students",
        },
    },
    {
        "name": "John Wayne Gacy Jr.",
        "known_as": ["The Killer Clown"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/John_Wayne_Gacy_mug_shot.jpg/220px-John_Wayne_Gacy_mug_shot.jpg",
        "birth_year": 1942,
        "birth_location": "Chicago, Illinois, USA",
        "murder_count_proved": 33,
        "murder_count_actual": 33,
        "country": "United States",
        "years_active_from": 1972,
        "years_active_to": 1978,
        "active_in_provinces": ["Illinois"],
        "method": "Lured victims to his home, often under the pretense of work or a social visit, before restraining them.",
        "sentence_details": "Convicted on 33 counts of murder (1980); sentenced to death. Executed by lethal injection on 10 May 1994.",
        "motive": "Not formally disclosed; case files describe a pattern tied to control and concealment of identity as a respected community figure.",
        "additional_info": "Performed as 'Pogo the Clown' at community events, which contributed to extensive media coverage. Buried 26 victims in the crawl space of his home.",
        "status": "deceased",
        "caught_by": "Investigation into the disappearance of 15-year-old Robert Piest (Dec 1978) traced back to Gacy, leading to a search of his property.",
        "victim_stats": {
            "female": 0, "male": 33,
            "under 18": 20, "18-30": 13, "31-45": 0, "46-60": 0, "above 60": 0,
            "major_occupation": "students / labourers",
        },
    },
    {
        "name": "Aileen Carol Wuornos",
        "known_as": ["Damsel of Death"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Aileen_Wuornos_mug_shot.jpg/220px-Aileen_Wuornos_mug_shot.jpg",
        "birth_year": 1956,
        "birth_location": "Rochester, Michigan, USA",
        "murder_count_proved": 6,
        "murder_count_actual": 7,
        "country": "United States",
        "years_active_from": 1989,
        "years_active_to": 1990,
        "active_in_provinces": ["Florida"],
        "method": "Worked as a sex worker along highways and shot clients during or after encounters.",
        "sentence_details": "Convicted on 6 counts of murder (1992-93); sentenced to death. Executed by lethal injection on 9 October 2002.",
        "motive": "Claimed self-defense in most cases, stating victims became violent; courts largely rejected this defense.",
        "additional_info": "One of the few widely documented female serial killers in the United States; subject of extensive documentary coverage.",
        "status": "deceased",
        "caught_by": "Pawned a victim's belongings, which were traced back to her through pawn shop records.",
        "victim_stats": {
            "female": 0, "male": 6,
            "under 18": 0, "18-30": 0, "31-45": 2, "46-60": 3, "above 60": 1,
            "major_occupation": "truck drivers / travelling salesmen",
        },
    },
    {
        "name": "Harold Frederick Shipman",
        "known_as": ["Dr Death", "The Angel of Death"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Harold_Shipman.jpg/220px-Harold_Shipman.jpg",
        "birth_year": 1946,
        "birth_location": "Nottingham, England, UK",
        "murder_count_proved": 15,
        "murder_count_actual": 250,
        "country": "United Kingdom",
        "years_active_from": 1971,
        "years_active_to": 1998,
        "active_in_provinces": ["Greater Manchester", "West Yorkshire"],
        "method": "As a trusted general practitioner, administered lethal doses of the opioid diamorphine to patients during home visits, then falsified death certificates and medical records to attribute deaths to natural causes.",
        "sentence_details": "Convicted on 15 counts of murder and 1 count of forgery (31 January 2000); sentenced to life imprisonment with a whole life order. A public inquiry (the Shipman Inquiry) later attributed roughly 250 deaths to him.",
        "motive": "Never disclosed; he denied guilt throughout. Theories include a euthanasia-like superiority complex and possible ties to his mother's death from cancer.",
        "additional_info": "Considered one of the most prolific serial killers in modern history by estimated victim count. His case prompted major reforms to UK death-certification and prescription-monitoring systems.",
        "status": "deceased",
        "caught_by": "A suspicious forged will left by victim Kathleen Grundy naming Shipman as beneficiary triggered a police investigation and exhumation.",
        "victim_stats": {
            "female": 12, "male": 3,
            "under 18": 0, "18-30": 0, "31-45": 0, "46-60": 2, "above 60": 13,
            "major_occupation": "retired / elderly patients",
        },
    },
    {
        "name": "Jeffrey Lionel Dahmer",
        "known_as": ["The Milwaukee Cannibal", "The Milwaukee Monster"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Jeffrey_Dahmer_mugshot.jpg/220px-Jeffrey_Dahmer_mugshot.jpg",
        "birth_year": 1960,
        "birth_location": "Milwaukee, Wisconsin, USA",
        "murder_count_proved": 16,
        "murder_count_actual": 17,
        "country": "United States",
        "years_active_from": 1978,
        "years_active_to": 1991,
        "active_in_provinces": ["Ohio", "Wisconsin"],
        "method": "Lured men and boys to his home with offers of money or photographs, then drugged and strangled them; committed extensive acts of dismemberment, necrophilia, and cannibalism with the remains.",
        "sentence_details": "Convicted of 15 counts of murder in Wisconsin (Feb 1992) and 1 count in Ohio (May 1992); sentenced to 16 consecutive terms of life imprisonment without parole.",
        "motive": "Described by himself and evaluators as driven by a compulsion for total control over his victims, including in death; diagnosed with several personality disorders but ruled legally sane.",
        "additional_info": "Killed by a fellow inmate, Christopher Scarver, on 28 November 1994 while serving his sentence.",
        "status": "deceased",
        "caught_by": "An intended victim, Tracy Edwards, escaped Dahmer's apartment and flagged down police on 22 July 1991.",
        "victim_stats": {
            "female": 0, "male": 17,
            "under 18": 2, "18-30": 13, "31-45": 2, "46-60": 0, "above 60": 0,
            "major_occupation": "unemployed / various service jobs",
        },
    },
    {
        "name": "Andrei Romanovich Chikatilo",
        "known_as": ["The Rostov Ripper", "The Butcher of Rostov", "The Red Ripper"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Andrei_Chikatilo.jpg/220px-Andrei_Chikatilo.jpg",
        "birth_year": 1936,
        "birth_location": "Yabluchne, Sumy Oblast, Ukrainian SSR",
        "murder_count_proved": 52,
        "murder_count_actual": 56,
        "country": "Soviet Union / Russia",
        "years_active_from": 1978,
        "years_active_to": 1990,
        "active_in_provinces": ["Rostov Oblast", "Ukrainian SSR", "Uzbek SSR"],
        "method": "Approached vulnerable women and children at train and bus stations with a simple pretext, lured them to secluded wooded areas, then stabbed and mutilated them.",
        "sentence_details": "Convicted of 52 of 53 charged murders (15 October 1992); sentenced to death on all counts. Executed by gunshot on 14 February 1994.",
        "motive": "Linked by himself to sexual dysfunction; he reported achieving arousal only through extreme violence against victims.",
        "additional_info": "Soviet authorities' initial refusal to acknowledge that serial murder could occur in a communist society delayed his capture for years; an earlier suspect, Aleksandr Kravchenko, was wrongfully executed for one of Chikatilo's murders.",
        "status": "deceased",
        "caught_by": "Increased plainclothes surveillance at railway and bus stations; observed acting suspiciously near where his final victim's body was found (November 1990).",
        "victim_stats": {
            "female": 32, "male": 20,
            "under 18": 21, "18-30": 20, "31-45": 8, "46-60": 3, "above 60": 0,
            "major_occupation": "students / vagrants / runaways",
        },
    },
    {
        "name": "Pedro Alonso López",
        "known_as": ["Monster of the Andes"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Pedro_Alonso_Lopez.jpg/220px-Pedro_Alonso_Lopez.jpg",
        "birth_year": 1948,
        "birth_location": "Santa Isabel, Tolima, Colombia",
        "murder_count_proved": 110,
        "murder_count_actual": 300,
        "country": "Colombia / Ecuador / Peru",
        "years_active_from": 1969,
        "years_active_to": 1980,
        "active_in_provinces": ["Tungurahua", "Cotopaxi", "Chimborazo", "Pichincha", "Imbabura"],
        "method": "Targeted young girls, mainly from poor or indigenous communities, luring them away with small gifts before raping and strangling them.",
        "sentence_details": "Pled guilty to 110 murders in Ecuador (1980); sentenced to 16 years' imprisonment, the maximum allowed under Ecuadorian law at the time. Released in 1994 after 14 years for good behavior, briefly institutionalized in Colombia, then released in 1998.",
        "motive": "Described by himself as revenge-driven, tied to his own childhood sexual abuse; expressed no remorse in recorded interviews.",
        "additional_info": "Whereabouts unknown since around 1998-2002; considered a wanted fugitive in connection with a later murder. Illustrates how weak cross-border coordination allowed a single offender to operate across three countries.",
        "status": "suspected",
        "caught_by": "Apprehended in an Ambato, Ecuador marketplace in 1980 after being seen attempting to lead away a young girl; an undercover cellmate later obtained his confession.",
        "victim_stats": {
            "female": 110, "male": 0,
            "under 18": 110, "18-30": 0, "31-45": 0, "46-60": 0, "above 60": 0,
            "major_occupation": "children, not employed",
        },
    },
    {
        "name": "Dennis Lynn Rader",
        "known_as": ["BTK Killer", "BTK Strangler"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Dennis_Rader_mugshot.jpg/220px-Dennis_Rader_mugshot.jpg",
        "birth_year": 1945,
        "birth_location": "Pittsburg, Kansas, USA",
        "murder_count_proved": 10,
        "murder_count_actual": 10,
        "country": "United States",
        "years_active_from": 1974,
        "years_active_to": 1991,
        "active_in_provinces": ["Kansas"],
        "method": "Broke into victims' homes, bound them, and killed them by strangulation or suffocation; self-styled his method and nickname as 'Bind, Torture, Kill' (BTK).",
        "sentence_details": "Pled guilty to 10 counts of first-degree murder (2005); sentenced to 10 consecutive life terms, a minimum of 175 years without parole.",
        "motive": "Described his killings as driven by long-standing violent sexual fantasies dating to childhood; showed no clear external motive beyond compulsion.",
        "additional_info": "Went dormant for over a decade before resurfacing in 2004 with taunting letters to media, ultimately leading to his identification via a traceable computer disk.",
        "status": "convicted",
        "caught_by": "A floppy disk he sent to a TV station in 2005 was traced to a computer at his church, leading investigators to match his DNA to crime-scene evidence.",
        "victim_stats": {
            "female": 8, "male": 2,
            "under 18": 2, "18-30": 4, "31-45": 1, "46-60": 1, "above 60": 1,
            "major_occupation": "homemakers / office workers",
        },
    },
    {
        "name": "Peter William Sutcliffe",
        "known_as": ["The Yorkshire Ripper"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Peter_Sutcliffe_mugshot.jpg/220px-Peter_Sutcliffe_mugshot.jpg",
        "birth_year": 1946,
        "birth_location": "Bingley, West Yorkshire, England, UK",
        "murder_count_proved": 13,
        "murder_count_actual": 13,
        "country": "United Kingdom",
        "years_active_from": 1975,
        "years_active_to": 1980,
        "active_in_provinces": ["West Yorkshire", "Greater Manchester"],
        "method": "Attacked victims, mostly women walking alone at night, from behind with a hammer, then inflicted further injuries with a knife or screwdriver.",
        "sentence_details": "Convicted of 13 counts of murder and 7 of attempted murder (22 May 1981); sentenced to 20 concurrent life terms, converted to a whole life order in 2010.",
        "motive": "Claimed at trial to be acting on divine instruction to kill sex workers; the claim was rejected by the jury despite a paranoid schizophrenia diagnosis.",
        "additional_info": "Died in prison on 13 November 2020. The case is widely cited as an example of investigative failures, including police interviewing him nine times before his eventual arrest.",
        "status": "deceased",
        "caught_by": "Stopped by police on 2 January 1981 for false number plates while with a sex worker; murder weapons were found nearby the next day.",
        "victim_stats": {
            "female": 13, "male": 0,
            "under 18": 1, "18-30": 7, "31-45": 4, "46-60": 1, "above 60": 0,
            "major_occupation": "sex workers",
        },
    },
]


def run():
    db = SessionLocal()
    try:
        if db.query(models.Killer).count() > 0:
            print("Database already has data — skipping seed.")
            return
        for entry in SAMPLE_KILLERS:
            killer = models.Killer(**entry)
            db.add(killer)
        db.commit()
        print(f"Seeded {len(SAMPLE_KILLERS)} killer records.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
