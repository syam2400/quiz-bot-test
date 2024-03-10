
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST



def generate_bot_responses(message, session):
    bot_responses = []
    
    print(session.get('score'))
    current_question_id = session.get("current_question_id")
 
    if not current_question_id:
        session['score'] = 0  
        session.save()
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    
    try:
        user_answer = int(answer) 
        if  0 < user_answer <= 4 and current_question_id:
           
            user_index = user_answer - 1
            current_question = PYTHON_QUESTION_LIST[current_question_id-1]
          
            if current_question['options'][user_index] == current_question['answer']:
               
     
                session['score'] = int(session.get('score')) + 1
                session.save()
                return True, ""
            else:
             
                  return True, "incorrect answer"
        else:
                  return True, "wrong entry"
        
    except:
      return True, "wrong entry"
       
       

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    ''' 

    if not current_question_id:
        current_question_id = 0
        questions = PYTHON_QUESTION_LIST[current_question_id]
   
        options_with_numbers = "<br>".join([f"{index + 1}. {option}" for index, option in enumerate(questions['options'])])
        current_question = f"{questions['question_text']} <br><br> Options: <br>" + options_with_numbers

        return current_question,1
    else:
        try:
            questions = PYTHON_QUESTION_LIST[int(current_question_id)]
    
            options_with_numbers = "<br>".join([f"{index + 1}. {option}" for index, option in enumerate(questions['options'])])
            current_question = f"{questions['question_text']} <br><br> Options: <br>" + options_with_numbers
    
            id = current_question_id + 1
            return current_question, id
        except:
            return 0, current_question_id




def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.

    '''
    total = session.get('score') 
    return f"You scored: {total}"
