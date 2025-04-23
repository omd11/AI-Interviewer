from openai import OpenAI
import communication
import random
import os
    
class InterviewSession():
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.interview_gen = OpenAI(api_key=self.api_key)
        self.difficulty = None
        self.industry = None
        self.role = None
        self.questions_no = None
        self.resume_uploaded = False
        self.follow_up = False
        self.overall_evaluation = None
        self.interviewer = None
        self.debug_mode = True

        
        self.questions = []

        self.answers = []

        self.current_question = 0
        self.current_answer = 0

    def setup_interviewer(self):
        self.interviewer = Interviewer(self.interview_gen, self.difficulty, self.industry, self.role,self.log,self.questions,self.current_question,self.overall_evaluation,self.transcript_form,self.debug_mode)

    def setup_questions(self):
        if self.debug_mode: 
            self.interviewer.questions = self.questions = ["What experience do you have with network security protocols and how have you implemented them in your previous roles?","Can you describe a time when you identified a security vulnerability and the steps you took to mitigate it?","What cybersecurity tools and technologies are you most proficient in, and how have you utilized them in past projects?" , "How do you stay updated on the latest cybersecurity threats and trends?" , "Can you walk me through your process for conducting a risk assessment?" , "Describe a challenging incident you\'ve dealt with in your role as a cybersecurity analyst and how you resolved it.","What is your approach to incident response and what key steps do you follow?"]
        else:
            self.interviewer.questions = self.questions = self.interview_gen.responses.create(
                model="gpt-4o-mini",
                input=f"create a list of {self.questions_no} interview questions for the {self.industry} industry for the role of {self.role}. \
                The output should be a python list of strings delimited by '|' instead of ',' and should be written as if asked in the first person \
                    . If {self.resume_uploaded} = True, 1 or more questions may be related work experience, skills or projects as listed in the resume.\
                The questions should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the \
                {self.difficulty} difficulty level. The output should not contain any variable declaration, equality signs or square brackets."
            ).output_text.split("|")

    def begin_interview(self,transcript_form):
        self.transcript_form = transcript_form
        transcript_form.transcript_label.setText("New Interview Session: ")

        self.log = open("interview_log.txt", "a")
        self.log.write("New Interview Session\n")
        self.overall_evaluation = []
        self.setup_interviewer()
        self.setup_questions()
        self.interviewer.introduction()

        print(self.current_question)
        while self.current_question < len(self.questions):
            self.interviewer.ask_question(self.current_question)
            answer = communication.user_turn()
            transcript_form.transcript_label.setText(f"{transcript_form.transcript_label.text()} \n Interviewee: {answer}")
            self.log.write(f"Interviewee: {answer}\n")
            
            if self.follow_up:
                match self.difficulty:
                    case "Easy":
                        self.interviewer.evaluate_answer(answer)
                        if random.random() < 0.2:
                            followup = self.interview_gen.responses.create(
                                model="gpt-4o-mini",
                                input=f"Create a follow up question for the following answer: ({answer}). The follow up question should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the {self.difficulty} difficulty level.").output_text
                            communication.interviewer_turn(followup)
                            answer = communication.user_turn()
                            transcript_form.transcript_label.setText(f"{transcript_form.transcript_label.text()} \n Interviewee: {answer}")
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
                            transcript_form.transcript_label.setText(f"{transcript_form.transcript_label.text()} \n Interviewee: {answer}")
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
                            transcript_form.transcript_label.setText(f"{transcript_form.transcript_label.text()} \n Interviewee: {answer}")
                            self.log.write(f"Interviewee: {answer}\n")
                            self.interviewer.evaluate_answer(answer)
            else:
                self.interviewer.evaluate_answer(answer)


            self.current_question += 1

  



class Interviewer(InterviewSession):
    def __init__(self, interview_gen=None, difficulty=None, industry=None, role=None,log=None,questions=None,current_question=None,overall_evaluation =None,transcript_form=None,debug_mode=None):
        self.interview_gen = interview_gen
        self.difficulty = difficulty
        self.industry = industry
        self.role = role
        self.log = log
        self.questions = questions
        self.current_question = current_question
        self.overall_evaluation = overall_evaluation
        self.transcript_form = transcript_form
        self.debug_mode = debug_mode

        

        self.interviewer_persona = self.interview_gen.responses.create(
        model="gpt-4o-mini",
        input=f"Create a persona for an interviewer in the {self.industry} industry for the role of {self.role}. \
        The output should be a python list delimited with '|' instead of ',' . The first string should be the name of the interviewer, the second string should be a short description of the interviewer's goals,\
        the third string should be a short description of the interviewer's personality traits, and the fourth string should be a short description of the interviewer's interview style.\
        The interviewer's goals, personality traits and interview style should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the \
        {self.difficulty} difficulty level. The output should only be the list, without any variable, equality signs or square brackets").output_text.split("|")

        self.interviewer_name = self.interviewer_persona[0]
        self.interviewer_goals = self.interviewer_persona[1]
        self.interviewer_personality = self.interviewer_persona[2]
        self.interviewer_style = self.interviewer_persona[3]

    def ask_question(self,qno:int):
            communication.interviewer_turn(self.questions[qno])
            self.transcript_form.transcript_label.setText(f"{self.transcript_form.transcript_label.text()} \n Interviewer: {self.questions[qno]}")
            self.log.write(f"Interviewer: {self.questions[qno]}\n")
            

    def evaluate_answer(self,answer):
        response = self.interview_gen.responses.create(
            model="gpt-4o-mini",
            input=f"From the perspective of the interviewer and taking into consideration their goals: ({self.interviewer_goals}), their personality traits: ({self.interviewer_personality}) \
            and their interview style: ({self.interviewer_style}), acknowledge or make a comment about the following interviewee answer: ({answer}) Do not ask any further questions. This answer is in respond to your question\
            {self.questions[self.current_question]}. Your response should be a string in the first entry of a Python list. In the second entry of the python list should be an evaluation score of the \
            response from 1-10. In the third entry of the python list should be a short description of the strengths and weaknesses of the answer. In the fourth entry of the python list should \
            be a short description of how the answer could be improved. The evaluation should be relevant to the {self.industry} industry, the {self.role} role and should be appropriate for the \
            {self.difficulty} difficulty level. The output should only be the list delimited with '|' instead of ',' , without any variable, equality signs or square brackets.").output_text.split("|")
        self.overall_evaluation.extend(response[1:])
        self.transcript_form.transcript_label.setText(f"{self.transcript_form.transcript_label.text()} \n Interviewer: {response[0]}")
        self.log.write(f"Interviewer: {response[0]}\n")
        communication.interviewer_turn(response[0])

    def introduction(self):
        if self.debug_mode:
            intro = "Hello, I'm Jordan Smith, and I’m thrilled to be conducting your interview today for the cybersecurity analyst position. With over a decade of experience in the IT industry, particularly focusing on cybersecurity, I’ve had the opportunity to work on various projects that bolster organizational security posture and mitigate risks. I’m passionate about staying ahead of emerging threats and am eager to find a candidate who shares that commitment to safeguarding information and systems. I look forward to learning more about your background and skills today!"
        else:
            intro = self.interview_gen.responses.create(
            model="gpt-4o-mini",
            input=f"You are {self.interviewer_name}, a job interviewer in the {self.industry} industry for the role of {self.role}. \
            Introduce yourself to your interviewee in one paragraph").output_text
        print(f"Interviewer: {intro}\n")
        self.transcript_form.transcript_label.setText(f"{self.transcript_form.transcript_label.text()} \n Interviewer: {intro}")
        self.log.write(f"Interviewer: {intro}\n")
        communication.interviewer_turn(intro)

