from django.core.management.base import BaseCommand
from goalapp.models import MBTIExplanation

class Command(BaseCommand):
    help = 'Seed MBTIExplanation table with all 16 MBTI personality types.'

    def handle(self, *args, **options):
        data = [
                {
                    'type_code': 'ISTJ',
                    'description': 'ISTJs are dependable and detail-oriented individuals who value tradition and order.',
                    'explanation': 'The ISTJ, standing for Introverted, Sensing, Thinking, and Judging, represents a personality type characterized by an unwavering commitment to duty, precision, and the preservation of established systems, making them the backbone of any organization or community where reliability is paramount; their introverted nature draws them to solitary or small-group settings where they can concentrate deeply on tasks without external interruptions, allowing them to excel in roles requiring meticulous attention such as accounting, administration, or project management, while their sensing trait anchors them firmly in the present and past, relying on concrete data and proven methods rather than speculative ideas, complemented by a thinking preference that prioritizes logical analysis and objective decision-making over emotional considerations, and a judging aspect that instills a love for structure, schedules, and clear expectations; this combination often leads them to thrive in environments where they can implement and maintain order, such as in legal or logistical fields, where their ability to follow through on commitments is highly valued; however, their preference for stability can make them resistant to sudden changes or innovative approaches, potentially causing friction in dynamic settings, and their tendency to suppress emotions might distance them from deeper personal connections, suggesting that personal growth could involve embracing occasional spontaneity, experimenting with new perspectives, and cultivating emotional expressiveness to enrich both their professional and personal lives, thereby enhancing their adaptability and relationships.',

                    'growth_tips': [
                        'Embrace occasional spontaneity to broaden your perspective.',
                        'Practice expressing emotions to strengthen personal connections.',
                        'Consider experimenting with new methods to enhance flexibility.'
                    ],
                    'matches': 'Compatible with ESTP, ESFP, and other sensing types who appreciate their reliability.'
                },
                {
                    'type_code': 'ISTP',
                    'description': 'ISTPs are hands-on problem-solvers who enjoy exploring how things work.',
                    'explanation': 'The ISTP, representing Introverted, Sensing, Thinking, and Perceiving, embodies a pragmatic and resourceful personality type with an innate curiosity about the mechanics and functionality of the world around them, often excelling in hands-on problem-solving scenarios where their practical skills shine, such as in engineering, mechanics, or emergency response, with their introverted nature fostering a preference for working independently or with a trusted few, enabling intense focus and creativity without the pressure of social demands; their sensing trait keeps them grounded in the tangible present, allowing them to notice fine details and respond swiftly to immediate challenges, while their thinking preference drives them to make efficient, logical decisions based on observable evidence rather than emotional impulses, and their perceiving aspect grants them a flexible, adaptable approach that resists rigid schedules, encouraging exploration of diverse interests and spontaneous actions; this blend makes them adept at troubleshooting and innovating on the fly, often thriving in high-stakes situations where quick thinking is essential, yet their aversion to long-term planning or emotional depth can lead to difficulties in maintaining commitments or forming deep relationships, suggesting that growth might involve setting strategic goals, engaging more fully in emotional dialogues, and sharing their expertise to foster teamwork, thereby balancing their independence with a richer social and professional life.',

                    'growth_tips': [
                        'Engage in emotional conversations to build stronger bonds.',
                        'Set long-term goals to complement your adaptability.',
                        'Share your expertise with others to enhance teamwork.'
                    ],
                    'matches': 'Compatible with ESTJ, ESFJ, and other thinking types who value their problem-solving skills.'
                },
                {
                    'type_code': 'ISFJ',
                    'description': 'ISFJs are nurturing and loyal individuals who prioritize the needs of others.',
                    'explanation': 'The ISFJ, meaning Introverted, Sensing, Feeling, and Judging, is a compassionate and steadfast personality type defined by a profound dedication to caring for and supporting those in their orbit, often finding solace in quiet, familiar environments where their introverted nature allows them to focus on the well-being of others without overwhelming social exposure, utilizing their sensing trait to recall intricate details about people’s lives and preferences, which enhances their role as thoughtful caregivers in professions like nursing, teaching, or social work; their feeling preference guides their decisions through a lens of empathy and personal values, frequently placing the needs of family, friends, or colleagues above their own, while the judging aspect fosters a love for structure and routine that helps them maintain harmony and plan effectively, ensuring stability in their personal and professional spheres; this combination makes them pillars of their communities, often going above and beyond to ensure others feel supported, yet their self-sacrificing tendencies and sensitivity to criticism can lead to burnout or difficulty asserting their own needs, indicating that personal growth could involve setting healthy boundaries, embracing new experiences to build resilience, and seeking constructive feedback to bolster their confidence, ultimately allowing them to sustain their nurturing nature without compromising their own well-being.',

                    'growth_tips': [
                        'Practice asserting your own needs to maintain balance.',
                        'Explore new experiences to build resilience.',
                        'Seek feedback to grow beyond your comfort zone.'
                    ],
                    'matches': 'Compatible with ENTP, ENFP, and other intuitive types who appreciate their warmth.'
                },
                {
                    'type_code': 'ISFP',
                    'description': 'ISFPs are gentle, creative souls who live in the moment and express themselves through art.',
                    'explanation': 'The ISFP, standing for Introverted, Sensing, Feeling, and Perceiving, is a tender and imaginative personality type that finds profound joy in the sensory richness of the present moment, often retreating into their inner world to process emotions and ideas through their introverted nature, leveraging their sensing trait to savor experiences like music, visual art, or nature, which fuels their creative expressions in fields such as painting, design, or music; their feeling preference drives decisions based on personal values and a desire for harmony, guiding them to create works that resonate emotionally with others, while their perceiving aspect imbues them with a flexible, free-spirited approach that resists strict plans, allowing them to flow with inspiration and adapt to new artistic challenges; this makes them uniquely suited for roles where individuality and creativity flourish, yet their aversion to conflict and reluctance to engage in long-term planning can hinder progress in structured environments or relationships, suggesting that growth might involve setting gentle, achievable goals to provide direction, practicing calm conflict resolution to build confidence, and exploring structured projects to balance their artistic freedom with practical skills, thereby enhancing their ability to thrive in diverse settings.',


                    'growth_tips': [
                        'Set small, achievable goals to enhance focus.',
                        'Practice addressing conflict calmly to build confidence.',
                        'Explore structured projects to balance creativity.'
                    ],
                    'matches': 'Compatible with ENTJ, ESTJ, and other judging types who provide stability.'
                },
                {
                    'type_code': 'INFJ',
                    'description': 'INFJs are insightful and idealistic individuals driven by a desire to help others.',
                    'explanation': 'The INFJ, meaning Introverted, Intuitive, Feeling, and Judging, is a rare and deeply insightful personality type marked by a visionary outlook and an intense drive to improve the world, often retreating into solitary reflection due to their introverted nature to process complex emotions and ideas, while their intuitive trait enables them to perceive patterns, future possibilities, and the underlying motivations of others, inspiring them to pursue meaningful causes such as counseling, nonprofit work, or social reform; their feeling preference shapes their decisions with profound compassion and a strong moral compass, guiding them to prioritize the greater good, and their judging aspect helps them organize these insights into actionable, structured plans that bring their ideals to life, making them exceptional leaders in empathetic and transformative roles; however, their deep empathy can lead to emotional exhaustion or burnout, and their tendency to overthink or strive for perfection may create self-imposed pressure, indicating that personal growth involves establishing realistic boundaries to protect their energy, trusting their intuitive insights while grounding them in practical steps, and prioritizing self-care to sustain their idealistic vision without sacrificing their health, ultimately allowing them to effect lasting change with resilience.',

                    'growth_tips': [
                        'Set boundaries to prevent emotional exhaustion.',
                        'Trust your instincts while grounding them in action.',
                        'Practice self-care to maintain your idealism.'
                    ],
                    'matches': 'Compatible with ENTP, ENFP, and other intuitive types who share their vision.'
                },
                {
                    'type_code': 'INFP',
                    'description': 'INFPs are dreamy and principled individuals who seek authenticity and purpose.',
                    'explanation': 'The INFP, standing for Introverted, Intuitive, Feeling, and Perceiving, is a soulful and idealistic personality type guided by a rich inner world of values, dreams, and emotions, often spending time in introspective solitude due to their introverted nature to explore abstract concepts and future possibilities through their intuitive trait, which fuels their passion for creative pursuits like writing, art, or activism where they can express their unique perspective; their feeling preference directs their decisions toward authenticity and harmony, aligning their actions with deeply held principles, while their perceiving aspect keeps them open and adaptable, allowing them to embrace new ideas and experiences without rigid constraints, making them natural advocates for causes that resonate with their core beliefs; however, their tendency to avoid decisive action or struggle with criticism—seeing it as a threat to their identity—can impede progress or personal growth, suggesting that development might involve building confidence in their choices, viewing feedback as a tool for improvement, and integrating practical steps to transform their dreams into tangible outcomes, thereby strengthening their ability to navigate the world while staying true to themselves.',

                    'growth_tips': [
                        'Make decisions confidently to enhance self-assurance.',
                        'Address criticism as a learning opportunity.',
                        'Balance dreams with actionable steps.'
                    ],
                    'matches': 'Compatible with INTJ, ENTJ, and other thinking types who complement their ideals.'
                },
                {
                    'type_code': 'INTJ',
                    'description': 'INTJs are strategic and visionary thinkers who excel at long-term planning.',
                    'explanation': 'The INTJ, meaning Introverted, Intuitive, Thinking, and Judging, is a strategic and visionary personality type renowned for their ability to envision complex systems and devise innovative, long-term solutions, often preferring the solitude of their own thoughts or the company of a select few due to their introverted nature, which allows them to concentrate on abstract possibilities and future-oriented planning through their intuitive trait, a strength that shines in fields like science, technology, or entrepreneurship; their thinking preference ensures decisions are rooted in logic, efficiency, and objective analysis, avoiding emotional bias, while their judging aspect drives them to create detailed, structured plans to execute their visions, making them formidable leaders and problem-solvers who thrive in roles requiring foresight and precision; however, their tendency to appear aloof or dismissive of emotions can strain relationships, and their perfectionist streak may lead to frustration or burnout, indicating that growth could involve fostering collaboration to incorporate diverse perspectives, softening their critical approach to build stronger connections, and accepting imperfections to reduce stress, ultimately enhancing their leadership effectiveness and personal fulfillment.',

                    'growth_tips': [
                        'Collaborate more to leverage diverse perspectives.',
                        'Soften criticism to build better relationships.',
                        'Accept imperfections to reduce stress.'
                    ],
                    'matches': 'Compatible with INFP, ENFP, and other feeling types who balance their logic.'
                },
                {
                    'type_code': 'INTP',
                    'description': 'INTPs are analytical and curious individuals who love exploring ideas.',
                    'explanation': 'The INTP, standing for Introverted, Intuitive, Thinking, and Perceiving, is an analytical and inquisitive personality type with an insatiable thirst for understanding the underlying principles of the world, often immersing themselves in solitary thought due to their introverted nature to explore theoretical concepts and possibilities through their intuitive trait, a passion that propels them toward success in research, philosophy, or technology where intellectual exploration is key; their thinking preference drives them to dissect problems with objective logic and rigorous analysis, seeking truth over sentiment, while their perceiving aspect keeps them open to new ideas and resistant to fixed schedules, allowing for creative and flexible problem-solving; this combination makes them brilliant innovators and theorists, yet their struggle with follow-through on ideas or expressing emotions can leave projects unfinished or relationships distant, suggesting that growth might involve committing to actionable steps to see tangible results, engaging in emotional conversations to deepen connections, and setting deadlines to enhance productivity, thereby bridging the gap between their intellectual pursuits and practical outcomes.',

                    'growth_tips': [
                        'Follow through on ideas to see tangible results.',
                        'Express emotions to connect with others.',
                        'Set deadlines to enhance productivity.'
                    ],
                    'matches': 'Compatible with INFJ, ENFJ, and other feeling types who appreciate their intellect.'
                },
                {
                    'type_code': 'ESTP',
                    'description': 'ESTPs are energetic and action-oriented individuals who thrive in the moment.',
                    'explanation': 'The ESTP, meaning Extraverted, Sensing, Thinking, and Perceiving, is a vibrant and action-driven personality type that thrives in the heat of the moment, drawing energy from lively social interactions due to their extraverted nature, while their sensing trait keeps them sharply attuned to the present, enabling quick, practical responses to unfolding challenges in fields like sales, sports, or emergency services; their thinking preference guides decisions with a focus on logic and efficiency, ensuring they tackle problems with a no-nonsense approach, and their perceiving aspect imbues them with adaptability and a spontaneous spirit that resists rigid plans, making them adept at seizing opportunities as they arise; this blend equips them to excel in high-energy, real-time environments where their boldness and resourcefulness shine, yet their tendency to overlook long-term consequences or avoid deep emotional commitments can lead to instability or shallow relationships, suggesting that growth could involve planning for the future to ensure stability, nurturing emotional bonds for deeper connections, and reflecting before acting to curb impulsiveness, thereby creating a more balanced and sustainable lifestyle.',

                    'growth_tips': [
                        'Plan for the future to ensure stability.',
                        'Nurture emotional connections for deeper bonds.',
                        'Reflect before acting to avoid impulsiveness.'
                    ],
                    'matches': 'Compatible with ISTJ, ISFJ, and other judging types who provide structure.'
                },
                {
                    'type_code': 'ESTJ',
                    'description': 'ESTJs are organized and decisive leaders who value efficiency and tradition.',
                    'explanation': 'The ESTJ, standing for Extraverted, Sensing, Thinking, and Judging, is a commanding and organized personality type that excels at leading with confidence and maintaining order, drawing energy from taking charge in social and professional settings due to their extraverted nature, while their sensing trait roots them in practical, time-tested methods that ensure reliability in roles like management, law enforcement, or administration; their thinking preference drives decisions based on logic, fairness, and efficiency, prioritizing results over emotions, and their judging aspect fuels their passion for creating and enforcing structured plans and clear expectations, making them natural organizers who thrive in environments requiring discipline and direction; this combination makes them highly effective in upholding traditions and driving teams toward success, yet their rigidity and potential dismissal of unconventional ideas can limit innovation or alienate others, indicating that growth might involve embracing flexibility to adapt to change, listening to diverse viewpoints to broaden their approach, and balancing authority with empathy to enhance leadership and foster collaborative success.',

                    'growth_tips': [
                        'Embrace flexibility to adapt to change.',
                        'Listen to new ideas to broaden your approach.',
                        'Balance authority with empathy.'
                    ],
                    'matches': 'Compatible with ISTP, ISFP, and other perceiving types who complement their structure.'
                },
                {
                    'type_code': 'ESFP',
                    'description': 'ESFPs are outgoing and enthusiastic individuals who love entertaining others.',
                    'explanation': 'The ESFP, meaning Extraverted, Sensing, Feeling, and Perceiving, is a lively and charismatic personality type that radiates energy and joy, thriving on social engagement due to their extraverted nature, while their sensing trait heightens their appreciation for the present moment, immersing them in sensory delights like music, dance, or theater, which they often share in entertaining roles such as performance arts or hospitality; their feeling preference shapes decisions with a focus on emotions and the needs of those around them, fostering a warm and inclusive atmosphere, and their perceiving aspect lends them a spontaneous, adaptable spirit that embraces new experiences without strict plans, making them the life of any gathering; this combination allows them to excel in bringing people together and creating memorable moments, yet their avoidance of planning or deep self-reflection can lead to a lack of direction or unpreparedness for future challenges, suggesting that growth could involve setting personal goals to provide focus, reflecting on experiences to gain insight, and planning ahead to enhance reliability, thereby adding depth and stability to their vibrant lifestyle.',
                    'growth_tips': [
                        'Set goals to provide direction.',
                        'Reflect on experiences to gain insight.',
                        'Plan ahead to enhance reliability.'
                    ],
                    'matches': 'Compatible with INTJ, INFJ, and other intuitive types who offer depth.'
                },
                {
                    'type_code': 'ESFJ',
                    'description': 'ESFJs are warm and sociable individuals who excel at nurturing communities.',
                    'explanation': 'The ESFJ, standing for Extraverted, Sensing, Feeling, and Judging, is a warm-hearted and sociable personality type dedicated to fostering harmony and support within their communities, drawing energy from active engagement with others due to their extraverted nature, while their sensing trait enables them to notice and address practical needs with a keen eye for detail, often shining in caregiving roles like teaching, healthcare, or event planning; their feeling preference guides their decisions with empathy and a commitment to group well-being, ensuring they prioritize the happiness of those around them, and their judging aspect drives them to organize events, uphold traditions, and maintain structured routines that strengthen social bonds; this makes them indispensable pillars of their social circles, always ready to lend a hand or celebrate milestones, yet their discomfort with conflict and tendency to neglect personal boundaries can lead to stress or resentment, suggesting that growth might involve asserting their own needs to maintain balance, accepting differing opinions to broaden their perspective, and developing conflict resolution skills to navigate challenges, thereby sustaining their nurturing role with greater personal strength.',

                    'growth_tips': [
                        'Assert your needs to maintain balance.',
                        'Accept differing views to broaden your perspective.',
                        'Develop conflict resolution skills.'
                    ],
                    'matches': 'Compatible with INTP, ISTP, and other thinking types who balance their warmth.'
                },
                {
                    'type_code': 'ENFP',
                    'description': 'ENFPs are enthusiastic and imaginative individuals who inspire others with their ideas.',
                    'explanation': 'The ENFP, meaning Extraverted, Intuitive, Feeling, and Perceiving, is an enthusiastic and imaginative personality type brimming with creative energy, thriving on social interactions due to their extraverted nature, while their intuitive trait sparks a vision of future possibilities and innovative solutions that they eagerly share in fields like marketing, counseling, or entrepreneurship; their feeling preference shapes their decisions with a focus on personal values and enthusiasm, inspiring others with their passion, and their perceiving aspect keeps them open and adaptable, allowing them to explore a wide array of interests without being bound by strict plans; this combination makes them dynamic motivators and idea generators who light up any room, yet their difficulty with follow-through on projects or maintaining routines can hinder long-term success, indicating that growth could involve channeling their energy into completing tasks, establishing consistent habits to boost productivity, and committing to follow-through to turn their vibrant ideas into lasting impact, thereby fulfilling their potential as catalysts for change.',

                    'growth_tips': [
                        'Focus energy on completing tasks.',
                        'Establish routines to enhance productivity.',
                        'Commit to follow-through for lasting impact.'
                    ],
                    'matches': 'Compatible with INTJ, INFJ, and other judging types who provide structure.'
                },
                {
                    'type_code': 'ENFJ',
                    'description': 'ENFJs are charismatic and empathetic leaders who motivate others toward growth.',
                    'explanation': 'The ENFJ, standing for Extraverted, Intuitive, Feeling, and Judging, is a charismatic and empathetic leader whose natural ability to inspire and uplift others stems from their extraverted nature, which fuels their love for social engagement, while their intuitive trait allows them to envision potential in people and situations, guiding them toward transformative roles like teaching, coaching, or community leadership; their feeling preference drives decisions with deep compassion and a focus on group harmony, making them adept at fostering collaboration and emotional connections, and their judging aspect enables them to organize their insights into structured plans that propel others toward growth; this blend makes them exceptional motivators who can turn visions into reality, yet their tendency to neglect their own needs or take criticism personally can lead to burnout or self-doubt, suggesting that growth might involve prioritizing self-care to prevent exhaustion, building resilience against feedback to maintain confidence, and balancing others’ needs with their own to sustain their influential leadership, ultimately enhancing their ability to lead with enduring strength.',

                    'growth_tips': [
                        'Prioritize self-care to avoid burnout.',
                        'Build resilience against criticism.',
                        'Balance others’ needs with your own.'
                    ],
                    'matches': 'Compatible with INTP, ISTP, and other thinking types who complement their empathy.'
                },
                {
                    'type_code': 'ENTP',
                    'description': 'ENTPs are clever and innovative thinkers who love a good challenge.',
                    'explanation': 'The ENTP, meaning Extraverted, Intuitive, Thinking, and Perceiving, is a clever and innovative personality type that revels in intellectual challenges and spirited debates, drawing energy from engaging with others due to their extraverted nature, while their intuitive trait sparks a constant stream of new ideas and possibilities that they explore with enthusiasm in fields like entrepreneurship, law, or innovation; their thinking preference ensures decisions are grounded in logical analysis and creative problem-solving, avoiding emotional bias, and their perceiving aspect keeps them open to change and experimentation, allowing them to adapt and pivot with ease; this combination makes them dynamic thinkers and trailblazers who thrive in environments that reward quick wit and originality, yet their inconsistency in following through on ideas or lack of emotional depth can undermine long-term projects or relationships, suggesting that growth could involve focusing efforts to complete initiatives, nurturing emotional connections to balance their intellect, and practicing consistency to enhance reliability, thereby maximizing their potential as visionary leaders.',

                    'growth_tips': [
                        'Focus efforts on completing projects.',
                        'Nurture emotional connections for balance.',
                        'Practice consistency to enhance reliability.'
                    ],
                    'matches': 'Compatible with ISFJ, ESFJ, and other feeling types who ground their ideas.'
                },
                {
                    'type_code': 'ENTJ',
                    'description': 'ENTJs are bold and strategic leaders who drive others toward success.',
                    'explanation': 'The ENTJ, standing for Extraverted, Intuitive, Thinking, and Judging, is a bold and strategic personality type that commands attention and drives success, thriving on taking charge in social and professional arenas due to their extraverted nature, while their intuitive trait enables them to see long-term opportunities and complex systems, positioning them as visionary leaders in executive roles, politics, or business; their thinking preference ensures decisions are based on logic, efficiency, and strategic foresight, sidelining emotional considerations, and their judging aspect empowers them to implement structured plans with decisive action, making them adept at turning visions into tangible results; this blend makes them formidable organizers and motivators who excel in high-stakes environments, yet their dominance and impatience with slower paces can alienate team members or stifle creativity, indicating that growth might involve cultivating patience to enhance teamwork, collaborating to leverage diverse input, and balancing assertiveness with empathy to foster a more inclusive leadership style, ultimately strengthening their ability to lead with both authority and harmony.',

                    'growth_tips': [
                        'Cultivate patience to enhance teamwork.',
                        'Collaborate more to leverage diverse input.',
                        'Balance assertiveness with empathy.'
                    ],
                    'matches': 'Compatible with ISFP, INFP, and other perceiving types who complement their drive.'
                }
            ]


        for entry in data:
            obj, created = MBTIExplanation.objects.get_or_create(
                type_code=entry['type_code'],
                defaults={
                    'description': entry['description'],
                    'explanation': entry['explanation'],
                    'growth_tips': entry['growth_tips'],
                    'matches': entry['matches'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Created: {entry['type_code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Already exists: {entry['type_code']}"))
