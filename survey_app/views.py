from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from survey_app.models import News_article, Personal_info
from django.views.decorators.cache import cache_control
from django.contrib import messages
from survey_app.forms import Personal_infoForm
import random
import string
import re
import datetime
import ast
import json
import openai
from django.conf import settings
from openai import OpenAI
from collections import Counter


def index(request):

    print(">>>>> index <<<<<")
    # reset the session keys
    request.session.flush()
    request.session.modified = True
    
    request.session['person_id'] = 0
    
    if request.method == 'POST':
        form = Personal_infoForm(request.POST)
        form.fields['preferred_headline'].required = False
        form.fields['preferred_headline2'].required = False
        form.fields['preferred_headline3'].required = False
        
        if form.is_valid():
            print("index form is valid")
            
            # Save the 'name' field to the session or temporarily store it            
            request.session['username'] = form.cleaned_data['name']
           
            return redirect('personal_info')  # Redirect to the next step (step 2)
        
        else:
            print(form.errors) 
            form = Personal_infoForm()
    else:
        form = Personal_infoForm()
        form.fields['preferred_headline'].required = False
        form.fields['preferred_headline2'].required = False
        form.fields['preferred_headline3'].required = False
        
    print ("I dont knowwwwww")

    return render(request, 'index.html', {'form': form})
    
def personal_info(request):

    try:
        if request.method == 'POST':
            print("yes POST method")
            personl_info = Personal_infoForm(request.POST)
            print("get the form")
            
            # 'name' is not required at this step
            personl_info.fields['name'].required = False

            if personl_info.is_valid():
                print("form is valid")
                answer = personl_info.save(commit=False)

                rd_str = ''.join(random.choice(string.ascii_lowercase)
                                 for _ in range(5))
                time_now = datetime.datetime.now().strftime('%H%M%S')
                gene_session = 'dars'+time_now + '_'+str(answer.id)+rd_str
                personl_info.instance.session_id = gene_session

                answer = personl_info.save(commit=True)

                request.session['person_id'] = answer.id

                gene_session = 'dars'+time_now + '_'+str(answer.id)+rd_str
                # personl_info.instance.session_id = request.session['prolific_id']

                request.session['session_id'] = gene_session
                answer = personl_info.save(commit=True)

                request.session['person_id'] = answer.id
                print("(---->>> personal_info_view - person ID", request.session['person_id'])

                
                # Determine and save the preferred headline style
                headline_style = determine_headline_style(answer)

                answer.headline_style = headline_style
                answer.save()


                # create session variable "selected_articles"
                request.session['selected_articles'] = []

                return redirect('front_page')
        else:
            print("personal info form is invalid")
            personl_info = Personal_infoForm()
            # 'name' is not required at this step
            personl_info.fields['name'].required = False
            
            

        print("skip form is invalid")

        # Shuffle choices for each headline question
        for field in ['preferred_headline', 'preferred_headline2', 'preferred_headline3']:
            personl_info.fields[field].choices = random.sample(
                personl_info.fields[field].choices, len(personl_info.fields[field].choices))
            
            # explaination:
            # personl_info.fields = {'preferred_headline':django form field, 'preferred_headline2':django form field, 'preferred_headline3':django form field}
            #  personl_info.fields[field] =  personl_info.fields[preferred_headline],  personl_info.fields[preferred_headline2],  personl_info.fields[preferred_headline3]
           
            #  personl_info.fields[field].choices = [
            #  headline_choices = 
            # [ ('Forward reference', 'Kinas Økonomiske Fremtid: Usikkerheten som Følger Etter Gullalderen'),    
            #     ('Metaphor', 'Kinas Økonomiske Skute i Uvær: Rentekutt som Redningsflåte'),
            #     ('Question', 'Er Kinas økonomiske gullalder over for godt?') ],
            # [the same for headline_choices2], 
            # [the same for headline_choices3],
            # ]

        # print("personl_info['preferred_headline'] = ", personl_info['preferred_headline'])
        # personl_info['preferred_headline'] = 3 titles for the specific headline 
        
        # Shuffle the headline questions
        headline_questions = [
            ('preferred_headline', personl_info['preferred_headline']),
            ('preferred_headline2', personl_info['preferred_headline2']),
            ('preferred_headline3', personl_info['preferred_headline3'])
        ]

        random.shuffle(headline_questions)
        
    except Exception as e:
        print("An exception occurred" + str(e))
        return redirect('index')

    return render(request, 'personal_info.html', context={'form': personl_info, 'questions': headline_questions})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def front_page(request):

    print("(---->>> front_page_view_person ID", request.session['person_id'])

    # get the article list from the database
    all_articles = News_article.objects.all()

    articles_list = list(all_articles)
    random.shuffle(articles_list)

    # Try to fetch personal info and the manipulated headlines
    try:
        personal_info = Personal_info.objects.get(id=request.session['person_id'])
        
        #save the user_name that came from index() into the database
        personal_info.name = request.session['username']
        personal_info.save()
        
        headline_style = personal_info.headline_style  # Get the headline style
        print("preferred headline_style = ", headline_style)
        
        for article in articles_list:
            if article.style == headline_style:
                article.title = article.manipulated_title

    except Personal_info.DoesNotExist:
        manipulated_headlines = {}
        print("No Personal_info found for the user.")

    try:
        if request.method == "POST":
            if "next_button" in request.POST:
                return redirect('end_page')
    except Exception as e:
        print("An exception occurred" + str(e))
        return redirect('index')

    date_dict = {'article_list_': articles_list, 'selected_style':headline_style}
    
    return HttpResponse(render(request, 'front_page.html', context=date_dict))


def determine_headline_style(answer):

    # Get the preferred headline choices
    choices = [
        answer.preferred_headline,
        answer.preferred_headline2,
        answer.preferred_headline3,
    ]

    # Count the occurrences of each headline style
    count = Counter(choices)
    print("headline counter = ", count)

    # Get the most common headline style(s)
    most_common = count.most_common()
    print("most common headline = ", most_common)
    # [('forward_referencde', 2)('question', 1)]

    # If there is a tie, randomly select one of the tied styles

    if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:

        print("choices = ", choices)
        selected_style = random.choice(choices)
        print("selected style = ", selected_style)

    else:
        print("common style found")
        selected_style = most_common[0][0]
    print("Final selected style = ", selected_style)

    return selected_style

# This function is called to add an article to the selected_articles list


def read_later(request):

    print("(---->>> selected_articles", request.session['person_id'])

    print("$$$$$$$$$$$$$$$$$$$$$$$$_selected_articles_$$$$$$$$$$$$$$$$$$$$$$$$")

    # get the article's info which was added to read later from front_page.html or article.html
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        article_info = post_data.get("article_info")

    # convert string to dictionary {'id':154, 'paty':'D'}
    article_info = ast.literal_eval(article_info)

    # list of selected_articles for the active user
    selected_articles_list = request.session.get('selected_articles', [])

    # add the current article's info to the array of read_later articles
    selected_articles_list.append(article_info)

    request.session['selected_articles'] = selected_articles_list
    request.session.modified = True

    print("0000000")
    print(request.session['selected_articles'])

    # add the selected_articles_list to the person's information
    try:
        this_person = Personal_info.objects.get(
            id=request.session['person_id'])
        this_person.selected_articles_list = request.session['selected_articles']
        this_person.save()
        print("Saved in person's info")

    except Exception as e:
        print("clicked articles error: " + str(e))

    return render(request, 'end_page.html')



def end_page(request):
    try:
    # list of selected_articles for the active user
        this_person = Personal_info.objects.get(id=request.session['person_id'])
        selected_articles = this_person.selected_articles_list
        print("selected_articles= ",selected_articles)
        
        correct = 0
        wrong = 0
        
        if (selected_articles):
                
            selected_articles = ast.literal_eval(selected_articles)
            total_num_selected = len(selected_articles)
            
            for article in selected_articles:
                if article['style'] == this_person.headline_style:
                    correct += 1
            wrong = total_num_selected - correct
            
            this_person.score = correct
            this_person.save()
            
            print ("correct =", correct)
            print ("wrong =", wrong)  
        else:
            #if the time out before user selects any articles  
            total_num_selected = 0
            correct = 0
             

    except Exception as e:
        print("calculating score error: " + str(e))
    
    #Get the top 10 scores
    top_ten = Personal_info.objects.all().order_by('-score')[:5]
    
    score = {'correct':correct, 'total':total_num_selected, 'top_ten':top_ten}
        
    # return HttpResponse(render(request, 'end_page.html', context=score))
    return render(request, 'end_page.html', context=score)



def error_page(request):
    return render(request, 'error_page.html')


def remove_read_later(request):
    # get the article's info which was added to selected from front_page.html
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        article_info = post_data.get("article_info")

     # convert string to dictionary {'id':154, 'paty':'D'}
    article_info = ast.literal_eval(article_info)

    # list of selected articles for the active user
    selected_articles_list = request.session.get('selected_articles', [])

    # Remove the current article's info from the array of selected articles
    selected_articles_list = [
        article for article in selected_articles_list if article != article_info]

    request.session['selected_articles'] = selected_articles_list
    request.session.modified = True

    try:
        this_person = Personal_info.objects.get(
            id=request.session['person_id'])
        this_person.selected_articles_list = request.session['selected_articles']
        this_person.save()

    except Exception as e:
        print("clicked articles error: " + str(e))
    

    return render(request, 'end_page.html')








##################### Anders code #############





# def Anders_end_page(request):
#     # Get session ID from the request's session
#     session_id = request.session.get('session_id')
    
#     if not session_id:
#         # If there is no session_id, this is an error state, redirect to the start page or handle accordingly
#         return redirect('start_page')

#     # Fetch the user session from the database
#     user_session = UserSessions.objects.get(id=session_id)

#     # Convert the string from single quotes to double quotes to make it valid JSON
#     articles_clicked_democrat_increase = jsonify(user_session.clicked_articles_democrat_increase)
#     articles_clicked_republican_increase = jsonify(user_session.clicked_articles_republican_increase)
#     read_later_democrat_increase = jsonify(user_session.read_later_democrat_increase)
#     read_later_republican_increase = jsonify(user_session.read_later_republican_increase)

#     total_clicked_democrat_increase = len(articles_clicked_democrat_increase)
#     total_clicked_republican_increase = len(articles_clicked_republican_increase)
#     total_read_later_democrat_increase = len(read_later_democrat_increase)
#     total_read_later_republican_increase = len(read_later_republican_increase)

#     article_types_democrat_clicked = calculate_article_types(articles_clicked_democrat_increase)
#     article_types_republican_clicked = calculate_article_types(articles_clicked_republican_increase)
#     article_types_democrat_read_later = calculate_article_types(read_later_democrat_increase)
#     article_types_republican_read_later = calculate_article_types(read_later_republican_increase)

#     # Calculate averages from all sessions
#     averages_data = calculate_averages()

#     context = {
#         'party': user_session.party_preference,

#         'total_clicked_democrat_increase': total_clicked_democrat_increase,
#         'total_clicked_republican_increase': total_clicked_republican_increase,
#         'total_read_later_democrat_increase': total_read_later_democrat_increase,
#         'total_read_later_republican_increase': total_read_later_republican_increase,

#         'stats_democrat_increase_clicked': article_types_democrat_clicked,
#         'stats_republican_increase_clicked': article_types_republican_clicked,
#         'stats_democrat_increase_read_later': article_types_democrat_read_later,
#         'stats_republican_increase_read_later': article_types_republican_read_later,
        
#         **averages_data
#     }

#     return render(request, 'end_page.html', context)


# def jsonify(input):
#     if input:
#         try:
#             # Replace single quotes with double quotes and convert string to JSON
#             input = input.replace("'", '"')
#             clicked_articles = json.loads(input)
#         except json.JSONDecodeError:
#             # Handle the exception if it's not valid JSON even after replacement
#             clicked_articles = []
#             # Log an error message or handle it as appropriate
#     else:
#         clicked_articles = []
    
#     return clicked_articles


# def spot_end_page(request):
#     # Get session ID from the request's session
#     session_id = request.session.get('session_id')
    
#     if not session_id:
#         # If there is no session_id, this is an error state, redirect to the start page or handle accordingly
#         return redirect('start_page')

#     # Fetch the user session from the database
#     user_session = UserSessionSpotArticles.objects.get(id=session_id)

#     if (user_session.party_preference == "Democrat"):
#         # Calculate the score
#         selected_articles = jsonify(user_session.selected_articles_democrat)
#         user_score = calculate_score(selected_articles, user_session.party_preference)
#     elif (user_session.party_preference == "Republican"):
#         selected_articles = jsonify(user_session.selected_articles_republican)
#         user_score = calculate_score(selected_articles, user_session.party_preference)

#     # Update the score in the database
#     user_session.score = user_score
#     user_session.save()

#     # Get leaderboards for both parties
#     # top_democrats, top_republicans = get_leaderboards()
#     top_democrats = assign_ranks(list(UserSessionSpotArticles.objects.filter(party_preference='Democrat').order_by('-score')))
#     top_republicans = assign_ranks(list(UserSessionSpotArticles.objects.filter(party_preference='Republican').order_by('-score')))

#     # Prepare context for the template
#     context = {
#         'party': user_session.party_preference,

#         'user_score': user_score,
#         'top_democrats': top_democrats,
#         'top_republicans': top_republicans,
#         # ... any other context you need to pass ...
#     }


#     return render(request, 'spot_end_page.html', context)



# def assign_ranks(users):
#     rank = 0
#     last_score = None
#     cumulative_rank_increment = 0

#     for user in users:
#         if last_score is None or last_score > user.score:
#             last_score = user.score
#             rank += 1 + cumulative_rank_increment
#             cumulative_rank_increment = 0
#         else:
#             cumulative_rank_increment += 1
#         user.rank = rank

#     return users
