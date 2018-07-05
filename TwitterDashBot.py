# Dependencies
import tweepy
import time
from datetime import datetime, timezone
import pandas as pd
from ConfigTweetBot import consumer_key, consumer_secret, access_token, access_token_secret
# Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def Send_Tweet(message):
    try:
        if (len(message) < 281):
            if (not Tweets_Sent.get(message)):
                # Tweet the next quote
                api.update_status(message) # post the tweet 
                Tweets_Sent[message] = message # update the Tweets_Sent dictionery
                # print("successful post")

    except Exception as ex:
        # if the message was posted in the previous run it may still throw 
        # error do not post again
        Tweets_Sent[message] = message
        # print("unsuccessful post")      
        pass       

# Create function for tweeting
def QuoteItUp(index):
    if(index < len(quote_list)): # prevent index out of range
        Send_Tweet(quote_list[index]) # send the tweet on that index number within the quote_list
    
# Match the tweet with the Hashtag
def matcher_tweet(tweet):
    for tag in Target_Hash_Tags:
        if tag.lower() in tweet.lower(): #  make case insensitive
            return True  


# Create tweet function
def Send_user_Tweet(target_user):
    # get the tweets of the target_user (which is listed in the list List_of_handles_to_monitor)
    public_tweets = api.user_timeline(target_user, count=200, result_type="recent")

    for tweet in public_tweets:     
        # Appended the tweeted tweets in the dictionery within the list all_tweet_listing
        all_tweet_listing.append({  "Influencer":target_user,
                                    "Tweet":tweet["text"]                                   
                                })

    # convert the dictionery into a dataframe
    tweet_listing_pd = pd.DataFrame.from_dict(all_tweet_listing)
        
    # The matcher function is being passed to the apply() to search for tweets in the dictionery
    # to find the matching hashtag in the tweets of the target user.(The function any() returns true/false.)
    # If there is no collection found then the any() returns False 
    Matching_Tweets = tweet_listing_pd['Tweet'].apply(matcher_tweet)
    if (Matching_Tweets.any()):
        for row in tweet_listing_pd.iterrows():
            tweet_to_send = row[1]['Tweet']
            if(matcher_tweet(tweet_to_send)):
                Send_Tweet(tweet_to_send)
                 
                
def process_tweets():
    for target_user in List_of_handles_to_monitor:
        Send_user_Tweet(target_user)

# List of Health Quotes to be tweeted at 6:00 AM 
quote_list = [  'Time means a lot to me because, you see, I, too, am also a learner and am often lost in the joy of forever developing and simplifying. If you love life, don’t waste time, for time is what life is made up of',
                'Life is what happens when you’re busy making other plans',
                'Very little is needed to make a happy life; it is all within yourself, in your way of thinking.'  
                'All the money in the world can\'t buy you back good health.',
                'Top 15 Things Money Can’t BuyTime. Happiness. Inner Peace. Integrity. Love. Character. Manners. Health. Respect. Morals. Trust. Patience. Class. Common sense. Dignity.',
                'Keep your best wishes, close to your heart and watch what happens.',
                'Cakes are healthy too, you just eat a small slice.',
                'A fit, healthy body—that is the best fashion statement.',
                'A fit, healthy body—that is the best fashion statement.',
                'Let food be thy medicine and medicine be thy food.',
                'The individual who says it is not possible should move out of the way of those doing it.',
                'People use drugs, legal and illegal, because their lives are intolerably painful or dull. They hate their work and find no rest in their leisure. They are estranged from their families and their neighbors. It should tell us something that in healthy societies drug use is celebrative, convivial, and occasional, whereas among us it is lonely, shameful, and addictive. We need drugs, apparently, because we have lost each other.',
                'We are healthy only to the extent that our ideas are humane.',
                'One rarely falls in love without being as much attracted to what is interestingly wrong with someone as what is objectively healthy.',
                'You are not a mistake. You are not a problem to be solved. But you won\'t discover this until you are willing to stop banging your head against the wall of shaming and caging and fearing yourself.',
                'Healthy citizens are the greatest asset any country can have.',
                'Happiness is part of who we are. Joy is the feeling.',
                'Money cannot buy health, but I\'d settle for a diamond-studdedwheelchair.',
                'When you believe without knowing you believe that you are damaged at your core, you also believe that you need to hide that damage for anyone to love you. You walk around ashamed of being yourself. You try hard to make up for the way you look, walk, feel. Decisions are agonizing because if you, the person who makes the decision, is damaged, then how can you trust what you decide? You doubt your own impulses so you become masterful at looking outside yourself for comfort. You become an expert at finding experts and programs, at striving and trying hard and then harder to change yourself, but this process only reaffirms what you already believe about yourself -- that your needs and choices cannot be trusted, and left to your own devices you are out of control.',
                'Wine is the most healthful and most hygienic of beverages.',
                'Don\'t destroy yourself by allowing negative people add gibberish and debris to your character, reputation, and aspirations. Keep all dreams alive but discreet, so that those with unhealthy tongues won\'t have any other option than to infest themselves with their own diseases.',
                'Healthy is merely the slowest rate at which one can die.',
                'The best doctor gives the least medicine.',
                'The \'i\' in illness is isolation, and the crucial letters in wellness is \'we\'.',
                'Dieting is the only game where you win when you lose!',
                'As for butter versus margarine, I trust cows more than chemists.',
                'Your imagination is your preview to life\'s coming attractions.',
                'A fit, healthy body-- that is the best fashion statement.',
                'A diet is the penalty we pay for exceeding the feed limit.',
                'Success is getting what you want, happiness is wanting what you get.',
                'Early to bed and early to rise, makes a man healthy wealthy and wise.',
                'Physical fitness is not only one of the most important keys to a healthy body, it is the basis of dynamic and creative intellectual activity.',
                'The greatest wealth is Health.',
                'Let food be thy medicine and medicine be thy food',
                'Just because you’re not sick doesn’t mean you’re healthy',
                'Those who think they have no time for exercise will sooner or later have to find time for illness.',
                'If you don’t take care of your body, where are you going to live?.',
                'Life expectancy would grow by leaps and bounds if green vegetables smelled as good as bacon.'
                'Health is a state of complete harmony of the body, mind and spirit. When one is free from physical disabilities and mental distractions, the gates of the soul open.',
                'If you can’t pronounce it, don’t eat it',
                'In order to change we must be sick and tired of being sick and tired.',
                'Health is like money, we never have a true idea of its value until we lose it.',
                'Time And health are two precious assets that we don’t recognize and appreciate until they have been depleted.',
                'From the bitterness of disease man learns the sweetness of health.',
                'Health and cheerfulness naturally beget each other.',
                'Take care of your body. It’s the only place you have to live.',
                'Your body is a temple, but only if you treat it as one.',
                'Mainstream medicine would be way different if they focused on prevention even half as much as they focused on intervention…',
                'Our bodies are our gardens – our wills are our gardeners.',
                'The best and most efficient pharmacy is within your own system.',
                'Health is not simply the absence of sickness.',
                'My own prescription for health is less paperwork and more running barefoot through the grass',
                'The more you eat, the less flavor; the less you eat, the more flavor.',
                'The doctor of the future will no longer treat the human frame with drugs, but rather will cure and prevent disease with nutrition.',
                'An apple a day keeps the doctor away',
                'A merry heart doeth good like a medicine, but a broken spirit dries the bones..',
                'True healthcare reform starts in your kitchen, not in Washington',
                'The only way to keep your health is to eat what you don’t want, drink what you don’t like, and do what you’d rather not.',
                'To insure good health: eat lightly, breathe deeply, live moderately, cultivate cheerfulness, and maintain an interest in life.',
                'A man too busy to take care of his health is like a mechanic too busy to take care of his tools.',
                'To keep the body in good health is a duty, for otherwise we shall not be able to trim the lamp of wisdom, and keep our mind strong and clear. Water surrounds the lotus flower, but does not wet its petals.',
                'Now there are more overweight people in America than average-weight people. So overweight people are now average. Which means you’ve met your New Year’s resolution.',
                'Don’t eat anything your great-great grandmother wouldn’t recognize as food. There are a great many food-like items in the supermarket your ancestors wouldn’t recognize as food.. stay away from these',
                'Health is a relationship between you and your body',
                'He who takes medicine and neglects to diet wastes the skill of his doctors.',
                'Sickness comes on horseback but departs on foot.',
                'Diseases of the soul are more dangerous and more numerous than those of the body.',
                'A good laugh and a long sleep are the best cures in the doctor’s book.',
                'Water, air and cleanliness are the chief articles in my pharmacopoeia.',
                'Health of body and mind is a great blessing, if we can bear it.',
                'Today, more than 95 percent of all chronic disease is caused by food choice, toxic food ingredients, nutritional deficiencies and lack of physical exercise.',
                'It’s bizarre that the produce manager is more important to my children’s health than the pediatrician.',
                'Healing in a matter of time, but it is sometimes also a matter of opportunity.',
                'The part can never be well unless the whole is well.',
                'Health is merely the slowest way someone can die.',
                'By cleansing your body on a regular basis and eliminating as many toxins as possible from your environment, your body can begin to heal itself, prevent disease, and become stronger and more resilient than you ever dreamed possible!',
             ]


Tweets_Sent = {}

# list of Hashtags being monitered
Target_Hash_Tags = ['#HarvardHealth','#WeightLoss','#Drug','#Medicine','#inflammation','#hcsm','#digitalhealth','#Exercise','#Health','#Diseases',
'#hcsmeu','#doctorsday','#NNM','#skincare','#pharmacy','#PlasticSurgery','#pharma','#ONC','#massagetherapy','#SelfCare','#KeepTalkingMH',
'#publichealth','#medicine','#SupportRadiopaedia','#AllTeachAllLearn','#patientcentric','#Lymphoma','#Lyphoma','#BTSM','#ADHD',
'#hidradenitissuppurativa','#MultipleSclerosis','#NeuroendocrineCancer','#Diabetes','#Migraine','#ChildhoodCancer','#ALS','#LupusChat',
'#MentalHealthPRU','#GenomicsDisparities','#MentalHealthPRU','#MentalHealth','#InnovationSW','#Innovation','#WilmsTumor','#Tumor',
'#Wilms','#Spondyloarthritis','#Spondyl','#arthritis','#Spondylitis','#patientcentric','#AllTeachAllLearn','#EbolaDRC','#Ebola',
'#MentalHealthPRU','#MentalHealth','#GenomicsDisparities','#Genomics','#Genes','#BCSM','#LCSM','#Neuroendocrine','#Cancer','Endocrine',
'#Sclerosis','#SpinaBifida','#EhlersDanlosSyndromes','#accreta','#Dizziness','#Pneumonia','#PreventingTheFlu','#HendraVirus',
'#Influenza','#LCSM','#Legionnaires','#LungCancer','#BrainInjury','#BrainTumor','#braintumors','#braintumour','#Preeclampsia',
'#preventaccreta','#ProstateCancer','#depresion','#Depression','#devlangdis','#EatingDisorder','#EatingDisorders','#EndEd',
'#Hypochondria','#DownSyndrome','#Dysautonomia','#Encephalitis','#Dementia','#DementiaChallenger','#PTSD','#Schizofrenie',
'#Schizophrenia','#Suicide','#trastornobipolar','#trich','#Trichotillomania','#WhatYouDontSee','#TesticularCancer','#uterinecancer',
'#varicocele','#wombcancer','#YeastInfection','#Legionnaires','#Fibroid','#Fibroids','#GynCSM','#HPV','#impotence','#Infertility',
'#AnorexiaNervosa','#ansiedad','#Anxiety','#AnxietyDisorder','#babyblues','#BDD','#bePNDaware','#Bipolar','#BipolarDisorder',
'#Alzheimer','#Alzheimers','#antiNMDAr','#Arachnoiditis','#Aspergers','#Ataxia','#Autism','#autismspectrum','#acousticneuroma',
'#AnosmiaHope','#Cholesteatoma','#Deafness','#EyeCancer','#glaucoma','#HearingLoss','#MacularDegeneratio','#Menieres','#myopiacontrol',
'#ocularmelanoma','#Tinnitus','#trachoma','#VisualSnow','#ACNE','#Alopecia','#AlopeciaAreata','#Bald','#Baldness','#basalcellcarcinoma',
'#cureEB','#deseosxpsoriasis','#Eczema','#euromelanoma17','#HairLoss','#Hidradenitis','#hidradenitissuppurativa','#Hives','#Ichthyosis',
'#KeratosisPilaris','#Leprosy','#Mastocytosis','#Melanoma','#merkelcellcarcinoma','#Pemphigus','#pemphigusvulgaris','#Psoriasis',
'#ringworm','#Shingles','#SkinCancer','#skintag','#StevensJohnsonSyndrome','#Urticaria','#pleuralEffusion','#Pneumonia',
'#PreventingTheFlu','#Resfriado','#Rhinitis','#SleepApnea','#StockportFluFighting','#Tuberculosis','#WhipLungCancer','#ChronicMigraine',
'#CIDP','#clusterheadache','#ClusterHeadaches','#curesma','#Dementia','#DementiaChallenger','#Demenz','#DownSyndrome','#Dysautonomia',
'#Encephalitis','#EndAlz','#Enxaqueca','#Epilepsy','#facialpain','#HemiplegicMigraine','#Huntingtonsdisease','#hydrocephalus','#IIH',
'#MemoryLoss','#Meningitis','#MuscularDystrophy','#MyalgicE','#MyastheniaGravis','#mypainisreal','#Narcolepsy','#Neuroblastoma',
'#Neuropathy','#Parkinsons','#Polio','#pseudobulbar','#RettSyndrome','#Seizures','#ShakenBabyFacts','#Shingles','#SleepDisorder',
'#SpinalCordInjury','#SpinalInjury','#StateofMS','#StiffPersonSyndrome','#Synesthesia','#TBI','#theARCchat','#TransverseMyelitis',
'#TrigeminalNeuralgia','#WeHaveMS','Psych','#AnorexiaNervosa','#ansiedad','#Anxiety','#AnxietyDisorder','#babyblues','#BDD','#bePNDaware',
'#Bipolar','#BipolarDisorder','#BPD','#Bulimia','#delirium','#depresion','#Depression','#devlangdis','#EatingDisorder','#EatingDisorders',
'#EndEd','#Hypochondria','#OCD','#PNDChat','#postpartumdepression','#PPD','#PPDchat','#problemgambling','#PTSD','#Schizofrenie',
'#Schizophrenia','#Suicide','#trastornobipolar','#trich','#Trichotillomania','#WhatYouDontSee','#WSPD','#wspd14','Reproductive',
'#accreta','#adenomyosis','#BacterialVaginosis','#CancerdeProstata','#CervicalCancer','#Endometriosis','#erectiledysfunction',
'#Fibroid','#Fibroids','#GynCSM','#HPV','#impotence','#Infertility','#MRKH','#OCAMChat','#OvarianCancer','#OVCA','#PCOS','#pcosaa',
'#PCSM','#Peyronies','#PeyroniesDisease','#PMDD','#PolycysticOvarianSyndrome','#Preeclampsia','#preventaccreta','#ProstateCancer',
'#prostatitis','#SecondaryInfertility','#TCisNoJoke','#TesticularCancer','#uterinecancer','#varicocele','#wombcancer','#YeastInfection',
'Respiratory','#A2ZCOPD','#ARDS45','#Asbestosis','#asma','#Asthma','#BetterLCLives','#BirdFlu','#Bronchitis','#Congestionnasal','#COPD',
'#DeviatedSeptum','#Enterovirus68','#Flu','#GPFAD2013','#Gripe','#Grippe','#H1N1','#HendraVirus','#Influenza','#LCSM','#Legionnaires',
'#LungCancer','#lungcancer101','#MdrTB','#MERS','#pleuralEffusion','#Pneumonia','#PreventingTheFlu','#Resfriado','#Rhinitis',
'#SleepApnea','#StockportFluFighting','#Tuberculosis','#WhipLungCancer','#SenseOrgans','#acousticneuroma','#AnosmiaHope','#Cholesteatoma',
'#Deafness','#EyeCancer','#glaucoma','#HearingLoss','#MacularDegeneration','#Menieres','#myopiacontrol','#ocularmelanoma','#Tinnitus',
'#trachoma','#VisualSnow','Skin','#ACNE','#Alopecia','#AlopeciaAreata','#Bald','#Baldness','#basalcellcarcinoma','#cureEB',
'#deseosxpsoriasis','#Eczema','#euromelanoma17','#HairLoss','#Hidradenitis','#hidradenitissuppurativa','#Hives','#Ichthyosis',
'#KeratosisPilaris','#Leprosy','#Mastocytosis','#Melanoma','#merkelcellcarcinoma','#Pemphigus','#pemphigusvulgaris','#Psoriasis',
'#ringworm','#Shingles','#SkinCancer','#skintag','#StevensJohnsonSyndrome']



# List of handles that we are monitoring
List_of_handles_to_monitor = ["@MonikerAsh","@ruchichandra26","@one171717","@IBaloyan","@KarnaniDeepa","@JAVillalbaUs","@JillStratton78",
"@JonathanGroth1","@data_stew","@Mike3dup","@TheRealAndrew19","@fervis_lauan","@pvenk14","@JingXu35625367","@MegNew2","@Pragati43524667"]

#['@HarvardHealth','@katyperry','@BarackObama','@taylorswift13','@ladygaga','@TheEllenShow','@Cristiano','@jtimberlake','@BritneySpears','@ArianaGrande','@ddlovato']

all_tweet_listing = []
counter = 0
Quote_Index = 0

# Set timer to run every 30 sec
while(True):
    try:
        current_time = datetime.now()
        if (current_time.hour == 6 and current_time.minute == 0):        
            QuoteItUp(counter)
            Quote_Index += 1
        else:
            process_tweets()
        # Monitor every 30 seconds    
        time.sleep(30)
        counter += 1
    except Exception as ex:
        # print("unsuccessful post")
        pass