from openai import OpenAI
import communication
import random
    
class InterviewSession():
    def __init__(self, api_key: str):
        self.interview_gen = OpenAI(api_key=api_key)
        self.difficulty = None
        self.industry = None
        self.role = None
        self.questions_no = None
        self.resume_uploaded = False
        self.follow_up = False
        self.overall_evaluation = list()
        self.log = open("interview_log.txt", "a")
        self.log.write("New Interview Session\n")
        
        self.questions = []

        self.answers = []

        self.current_question = 0
        self.current_answer = 0

    def setup_interviewer(self):
        self.interviewer = Interviewer(self.interview_gen,difficulty=self.difficulty, industry=self.industry, role=self.role)

    def setup_questions(self):
        self.questions = list(self.interview_gen.responses.create(
            model="gpt-4o-mini",
            input=f"create a list of {self.questions_no} interview questions for the {self.industry} industry for the role of {self.role}. \
            The output should be a python list of strings and should be written as if asked in the first person \
                . If {self.resume_uploaded} = True, 1 or more questions may be related work experience, skills or projects as listed in the resume.\
            The questions should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the \
            {self.difficulty} difficulty level."
        ).output_text)

    def begin_interview(self):
        self.setup_interviewer()
        self.setup_questions()
        self.interviewer.introduction()


        while self.current_question < len(self.questions):
            self.interviewer.ask_question(self.current_question)
            answer = communication.user_turn()
            self.log.write(f"Interviewee: {answer}\n")
            
            if self.followup:
                match self.difficulty:
                    case "Easy":
                        self.interviewer.evaluate_answer(answer)
                        if random.random() < 0.2:
                            followup = self.interview_gen.responses.create(
                                model="gpt-4o-mini",
                                input=f"Create a follow up question for the following answer: ({answer}). The follow up question should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the {self.difficulty} difficulty level.").output_text
                            communication.interviewer_turn(followup)
                            answer = communication.user_turn()
                            self.log.write(f"Interviewee: {answer}\n")
                            self.interviewer.evaluate_answer(answer)

                    case "Medium":
                        self.interviewer.evaluate_answer(answer)
                        if random.random() < 0.45:
                            followup = self.interview_gen.responses.create(
                                model="gpt-4o-mini",
                                input=f"Create a follow up question for the following answer: ({answer}). The follow up question should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the {self.difficulty} difficulty level.").output_text
                            
                            communication.interviewer_turn(followup)
                            answer = communication.user_turn()
                            self.log.write(f"Interviewee: {answer}\n")
                            self.interviewer.evaluate_answer(answer)

                    case "Hard":
                        self.interviewer.evaluate_answer(answer)
                        if random.random() < 0.7:
                            followup = self.interview_gen.responses.create(
                                model="gpt-4o-mini",
                                input=f"Create a follow up question for the following answer: ({answer}). The follow up question should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the {self.difficulty} difficulty level.").output_text
                            communication.interviewer_turn(followup)
                            answer = communication.user_turn()
                            self.log.write(f"Interviewee: {answer}\n")
                            self.interviewer.evaluate_answer(answer)
            else:
                self.interviewer.evaluate_answer(answer)


            self.current_question += 1

  



class Interviewer(InterviewSession):
    def __init__(self, interview_gen, difficulty, industry, role,overall_evaluation,log):
        super().__init__(difficulty, industry, role,overall_evaluation,log)
        self.interview_gen = interview_gen
        self.difficulty = difficulty
        self.industry = industry
        self.role = role
        self.overall_evaluation = overall_evaluation
        self.log = log
        

        self.interviewer_persona = self.interview_gen.responses.create(
        model="gpt-4o-mini",
        input=f"Create a persona for an interviewer in the {self.industry} industry for the role of {self.role}. \
        The output should be a python list strings. The first string should be the name of the interviewer, the second string should be a short description of the interviewer's goals,\
        the third string should be a short description of the interviewer's personality traits, and the fourth string should be a short description of the interviewer's interview style.\
        The interviewer's goals, personality traits and interview style should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the \
        {self.difficulty} difficulty level.").output_text

        self.interviewer_name = self.interviewer_persona[0]
        self.interviewer_goals = self.interviewer_persona[1]
        self.interviewer_personality = self.interviewer_persona[2]
        self.interviewer_style = self.interviewer_persona[3]

    def ask_question(self,qno:int):
            communication.interviewer_turn(self.questions[qno])
            self.log.write(f"Interviewer: {self.questions[qno]}\n")

    def evaluate_answer(self,answer):
        response = list(self.interview_gen.responses.create(
            model="gpt-4o-mini",
            input=f"From the perspective of the interviewer and taking into consideration their goals: ({self.interviewer_goals}), their personality traits: ({self.interviewer_personality}) \
            and their interview style: ({self.interviewer_style}), acknowledge or make a comment about the following interviewee answer: ({answer}). This answer is in respond to your question\
            {self.questions[self.current_question]}. Your response should be a string in the first entry of a Python list. In the second entry of the python list should be an evaluation score of the \
            response from 1-10. In the third entry of the python list should be a short description of the strengths and weaknesses of the answer. In the fourth entry of the python list should \
            be a short description of how the answer could be improved. The evaluation should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the \
            {self.difficulty} difficulty level.").output_text)
        self.overall_evaluation.extend(response[1:])
        self.log.write(f"Interviewer: {response[0]}\n")
        communication.interviewer_turn(response[0])

    def introduction(self):
        intro = self.interview_gen.responses.create(
        model="gpt-4o-mini",
        input=f"You are {self.interviewer_name}, a job interviewer in the {self.industry} industry for the role of {self.role}. \
        Introduce yourself to your interviewee. ").output_text

        self.log.write(f"Interviewer: {intro}\n")
        communication(self.interview_gen.responses.create(
        model="gpt-4o-mini",
        input=f"You are {self.interviewer_name}, a job interviewer in the {self.industry} industry for the role of {self.role}. \
        Introduce yourself to your interviewee. ").output_text)

