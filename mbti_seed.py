
from django.core.management.base import BaseCommand
from goalapp.models import MBTIExplanation

class Command(BaseCommand):
    help = 'Seed the MBTIExplanation table with all 16 MBTI types'

    def handle(self, *args, **kwargs):
        entries = [
            {
                "type_code": "ISTJ",
                "description": "ISTJs are dependable and detail-oriented individuals who value tradition and order.",
                "explanation": "The ISTJ, standing for Introverted, Sensing, Thinking, and Judging, represents a personality type characterized by an unwavering commitment to duty, precision, and the preservation of established systems...",
                "growth_tips": [
                    "Embrace occasional spontaneity to broaden your perspective.",
                    "Practice expressing emotions to strengthen personal connections.",
                    "Consider experimenting with new methods to enhance flexibility."
                ],
                "matches": "Compatible with ESTP, ESFP, and other sensing types who appreciate their reliability."
            },
            {
                "type_code": "ISTP",
                "description": "ISTPs are hands-on problem-solvers who enjoy exploring how things work.",
                "explanation": "The ISTP, representing Introverted, Sensing, Thinking, and Perceiving, embodies a pragmatic and resourceful personality type with an innate curiosity about the mechanics and functionality of the world around them...",
                "growth_tips": [
                    "Engage in emotional conversations to build stronger bonds.",
                    "Set long-term goals to complement your adaptability.",
                    "Share your expertise with others to enhance teamwork."
                ],
                "matches": "Compatible with ESTJ, ESFJ, and other thinking types who value their problem-solving skills."
            },
            {
                "type_code": "ISFJ",
                "description": "ISFJs are nurturing and loyal individuals who prioritize the needs of others.",
                "explanation": "The ISFJ, meaning Introverted, Sensing, Feeling, and Judging, is a compassionate and steadfast personality type defined by a profound dedication to caring for and supporting those in their orbit...",
                "growth_tips": [
                    "Practice asserting your own needs to maintain balance.",
                    "Explore new experiences to build resilience.",
                    "Seek feedback to grow beyond your comfort zone."
                ],
                "matches": "Compatible with ENTP, ENFP, and other intuitive types who appreciate their warmth."
            },
            {
                "type_code": "ISFP",
                "description": "ISFPs are gentle, creative souls who live in the moment and express themselves through art.",
                "explanation": "The ISFP, standing for Introverted, Sensing, Feeling, and Perceiving, is a tender and imaginative personality type that finds profound joy in the sensory richness of the present moment...",
                "growth_tips": [
                    "Set small, achievable goals to enhance focus.",
                    "Practice addressing conflict calmly to build confidence.",
                    "Explore structured projects to balance creativity."
                ],
                "matches": "Compatible with ENTJ, ESTJ, and other judging types who provide stability."
            },
            {
                "type_code": "INFJ",
                "description": "INFJs are insightful and idealistic individuals driven by a desire to help others.",
                "explanation": "The INFJ, meaning Introverted, Intuitive, Feeling, and Judging, is a rare and deeply insightful personality type marked by a visionary outlook and an intense drive to improve the world...",
                "growth_tips": [
                    "Set boundaries to prevent emotional exhaustion.",
                    "Trust your instincts while grounding them in action.",
                    "Practice self-care to maintain your idealism."
                ],
                "matches": "Compatible with ENTP, ENFP, and other intuitive types who share their vision."
            },
            {
                "type_code": "INFP",
                "description": "INFPs are dreamy and principled individuals who seek authenticity and purpose.",
                "explanation": "The INFP, standing for Introverted, Intuitive, Feeling, and Perceiving, is a soulful and idealistic personality type guided by a rich inner world of values, dreams, and emotions...",
                "growth_tips": [
                    "Make decisions confidently to enhance self-assurance.",
                    "Address criticism as a learning opportunity.",
                    "Balance dreams with actionable steps."
                ],
                "matches": "Compatible with INTJ, ENTJ, and other thinking types who complement their ideals."
            },
            {
                "type_code": "INTJ",
                "description": "INTJs are strategic and visionary thinkers who excel at long-term planning.",
                "explanation": "The INTJ, meaning Introverted, Intuitive, Thinking, and Judging, is a strategic and visionary personality type renowned for their ability to envision complex systems and devise innovative, long-term solutions...",
                "growth_tips": [
                    "Collaborate more to leverage diverse perspectives.",
                    "Soften criticism to build better relationships.",
                    "Accept imperfections to reduce stress."
                ],
                "matches": "Compatible with INFP, ENFP, and other feeling types who balance their logic."
            },
            {
                "type_code": "INTP",
                "description": "INTPs are analytical and curious individuals who love exploring ideas.",
                "explanation": "The INTP, standing for Introverted, Intuitive, Thinking, and Perceiving, is an analytical and inquisitive personality type with an insatiable thirst for understanding the underlying principles of the world...",
                "growth_tips": [
                    "Follow through on ideas to see tangible results.",
                    "Express emotions to connect with others.",
                    "Set deadlines to enhance productivity."
                ],
                "matches": "Compatible with INFJ, ENFJ, and other feeling types who appreciate their intellect."
            },
            {
                "type_code": "ESTP",
                "description": "ESTPs are energetic and action-oriented individuals who thrive in the moment.",
                "explanation": "The ESTP, meaning Extraverted, Sensing, Thinking, and Perceiving, is a vibrant and action-driven personality type that thrives in the heat of the moment...",
                "growth_tips": [
                    "Plan for the future to ensure stability.",
                    "Nurture emotional connections for deeper bonds.",
                    "Reflect before acting to avoid impulsiveness."
                ],
                "matches": "Compatible with ISTJ, ISFJ, and other judging types who provide structure."
            },
            {
                "type_code": "ESTJ",
                "description": "ESTJs are organized and decisive leaders who value efficiency and tradition.",
                "explanation": "The ESTJ, standing for Extraverted, Sensing, Thinking, and Judging, is a commanding and organized personality type that excels at leading with confidence and maintaining order...",
                "growth_tips": [
                    "Embrace flexibility to adapt to change.",
                    "Listen to new ideas to broaden your approach.",
                    "Balance authority with empathy."
                ],
                "matches": "Compatible with ISTP, ISFP, and other perceiving types who complement their structure."
            },
            {
                "type_code": "ESFP",
                "description": "ESFPs are outgoing and enthusiastic individuals who love entertaining others.",
                "explanation": "The ESFP, meaning Extraverted, Sensing, Feeling, and Perceiving, is a lively and charismatic personality type that radiates energy and joy...",
                "growth_tips": [
                    "Set goals to provide direction.",
                    "Reflect on experiences to gain insight.",
                    "Plan ahead to enhance reliability."
                ],
                "matches": "Compatible with INTJ, INFJ, and other intuitive types who offer depth."
            },
            {
                "type_code": "ESFJ",
                "description": "ESFJs are warm and sociable individuals who excel at nurturing communities.",
                "explanation": "The ESFJ, standing for Extraverted, Sensing, Feeling, and Judging, is a warm-hearted and sociable personality type dedicated to fostering harmony and support within their communities...",
                "growth_tips": [
                    "Assert your needs to maintain balance.",
                    "Accept differing views to broaden your perspective.",
                    "Develop conflict resolution skills."
                ],
                "matches": "Compatible with INTP, ISTP, and other thinking types who balance their warmth."
            },
            {
                "type_code": "ENFP",
                "description": "ENFPs are enthusiastic and imaginative individuals who inspire others with their ideas.",
                "explanation": "The ENFP, meaning Extraverted, Intuitive, Feeling, and Perceiving, is an enthusiastic and imaginative personality type brimming with creative energy...",
                "growth_tips": [
                    "Focus energy on completing tasks.",
                    "Establish routines to enhance productivity.",
                    "Commit to follow-through for lasting impact."
                ],
                "matches": "Compatible with INTJ, INFJ, and other judging types who provide structure."
            },
            {
                "type_code": "ENFJ",
                "description": "ENFJs are charismatic and empathetic leaders who motivate others toward growth.",
                "explanation": "The ENFJ, standing for Extraverted, Intuitive, Feeling, and Judging, is a charismatic and empathetic leader whose natural ability to inspire and uplift others stems from their extraverted nature...",
                "growth_tips": [
                    "Prioritize self-care to avoid burnout.",
                    "Build resilience against criticism.",
                    "Balance others’ needs with your own."
                ],
                "matches": "Compatible with INTP, ISTP, and other thinking types who complement their empathy."
            },
            {
                "type_code": "ENTP",
                "description": "ENTPs are clever and innovative thinkers who love a good challenge.",
                "explanation": "The ENTP, meaning Extraverted, Intuitive, Thinking, and Perceiving, is a clever and innovative personality type that revels in intellectual challenges and spirited debates...",
                "growth_tips": [
                    "Focus efforts on completing projects.",
                    "Nurture emotional connections for balance.",
                    "Practice consistency to enhance reliability."
                ],
                "matches": "Compatible with ISFJ, ISFJ, and other feeling types who ground their ideas."
            },
            {
                "type_code": "ENTJ",
                "description": "ENTJs are bold and strategic leaders who drive others toward success.",
                "explanation": "The ENTJ, standing for Extraverted, Intuitive, Thinking, and Judging, is a bold and strategic personality type that commands attention and drives success...",
                "growth_tips": [
                    "Cultivate patience to enhance teamwork.",
                    "Collaborate more to leverage diverse input.",
                    "Balance assertiveness with empathy."
                ],
                "matches": "Compatible with ISFP, INFP, and other perceiving types who complement their drive."
            },
        ]

        for entry in entries:
            obj, created = MBTIExplanation.objects.get_or_create(
                type_code=entry["type_code"],
                defaults={
                    "description": entry["description"],
                    "explanation": entry["explanation"],
                    "growth_tips": entry["growth_tips"],
                    "matches": entry["matches"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {entry['type_code']}"))
            else:
                self.stdout.write(f"Already exists: {entry['type_code']}")
