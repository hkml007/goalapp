MBTI_QUESTIONS = [
    # Extraversion (E) - 8 questions
    ("You enjoy vibrant social events with lots of people.", 'E'),
    ("You feel energized by meeting new people and networking.", 'E'),
    ("You prefer to lead conversations in group settings.", 'E'),
    ("You enjoy being the center of attention at social gatherings.", 'E'),
    ("You find it easy to strike up conversations with strangers.", 'E'),
    ("You thrive in busy, lively environments.", 'E'),
    ("You enjoy participating in group activities or team sports.", 'E'),
    ("You feel comfortable expressing yourself in large gatherings.", 'E'),
    # Introversion (I) - 8 questions
    ("You often think about what you should have said in a conversation long after it has taken place.", 'I'),
    ("You prefer to work alone rather than in a team.", 'I'),
    ("You feel more comfortable in small, familiar groups than large crowds.", 'I'),
    ("You need time alone to recharge after social interactions.", 'I'),
    ("You enjoy solitary activities like reading or writing.", 'I'),
    ("You prefer one-on-one conversations over group discussions.", 'I'),
    ("You often reflect deeply before sharing your thoughts.", 'I'),
    ("You feel drained after prolonged social events.", 'I'),
    # Sensing (S) - 8 questions
    ("You focus on the present moment rather than future possibilities.", 'S'),
    ("You prefer concrete facts and details over abstract ideas.", 'S'),
    ("You rely on past experiences to guide your decisions.", 'S'),
    ("You enjoy tasks that involve practical, hands-on activities.", 'S'),
    ("You notice details in your surroundings that others might miss.", 'S'),
    ("You prefer clear, step-by-step instructions for tasks.", 'S'),
    ("You value tried-and-true methods over experimental approaches.", 'S'),
    ("You focus on what is happening now rather than what might happen.", 'S'),
    # Intuition (N) - 8 questions
    ("You often spend time exploring unrealistic yet intriguing ideas.", 'N'),
    ("You are drawn to possibilities and what could be in the future.", 'N'),
    ("You enjoy thinking about abstract concepts and theories.", 'N'),
    ("You often notice patterns and connections others overlook.", 'N'),
    ("You like to imagine different scenarios and outcomes.", 'N'),
    ("You are excited by innovative and unconventional ideas.", 'N'),
    ("You enjoy exploring the 'big picture' rather than focusing on details.", 'N'),
    ("You often think about how current actions might shape the future.", 'N'),
    # Thinking (T) - 8 questions
    ("You make decisions based on logical analysis rather than emotions.", 'T'),
    ("You prioritize objective criteria when solving problems.", 'T'),
    ("You prefer to keep discussions focused on facts rather than feelings.", 'T'),
    ("You are comfortable giving constructive criticism to improve outcomes.", 'T'),
    ("You value fairness and consistency in decision-making.", 'T'),
    ("You analyze problems systematically before acting.", 'T'),
    ("You prefer debates that focus on logic over emotional appeals.", 'T'),
    ("You prioritize efficiency when completing tasks.", 'T'),
    # Feeling (F) - 8 questions
    ("If your friend is sad about something, your first instinct is to support them emotionally, not try to solve their problem.", 'F'),
    ("You consider your personal values when making decisions.", 'F'),
    ("You are deeply affected by others' emotions and experiences.", 'F'),
    ("You strive to maintain harmony in your relationships.", 'F'),
    ("You make decisions based on how they impact others’ feelings.", 'F'),
    ("You empathize easily with people in difficult situations.", 'F'),
    ("You prioritize relationships over strict adherence to rules.", 'F'),
    ("You feel fulfilled when helping others emotionally.", 'F'),
    # Judging (J) - 8 questions
    ("You prefer a planned and organized approach to life.", 'J'),
    ("You like to have a detailed schedule and stick to it.", 'J'),
    ("You feel satisfied when tasks are completed ahead of deadlines.", 'J'),
    ("You prefer to make decisions quickly to move forward.", 'J'),
    ("You organize your workspace to stay efficient.", 'J'),
    ("You prefer to have a clear plan before starting a project.", 'J'),
    ("You feel uneasy when plans are left open-ended.", 'J'),
    ("You like to set goals and follow through systematically.", 'J'),
    # Perceiving (P) - 8 questions
    ("Your travel plans are more likely to look like a rough list of ideas than a detailed itinerary.", 'P'),
    ("You enjoy keeping your options open and being flexible.", 'P'),
    ("You prefer spontaneous activities over planned ones.", 'P'),
    ("You feel comfortable adapting to last-minute changes.", 'P'),
    ("You enjoy exploring new possibilities without a fixed plan.", 'P'),
    ("You prefer to start projects and figure out details as you go.", 'P'),
    ("You feel constrained by strict schedules or routines.", 'P'),
    ("You like to keep your approach open to new opportunities.", 'P'),
]

MBTI_CHOICES = (
    ('SA', 'Strongly Agree'),
    ('A', 'Agree'),
    ('N', 'Neutral'),
    ('D', 'Disagree'),
    ('SD', 'Strongly Disagree'),
)

RESPONSE_WEIGHTS = {
    'SA': 2,
    'A': 1,
    'N': 0,
    'D': -1,
    'SD': -2,
}

ALL_MBTI_TYPES = ['ISTJ', 'ISTP', 'ISFJ', 'ISFP', 'INFJ', 'INFP', 'INTJ', 'INTP',
                  'ESTP', 'ESTJ', 'ESFP', 'ESFJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ']