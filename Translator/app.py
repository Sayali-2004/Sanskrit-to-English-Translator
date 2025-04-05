from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS pip install -U flask-cors
from googletrans import Translator

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

sanskrit_to_english_dict = {
    'धृतराष्ट्र उवाच |धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः |मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ||':'Dhritarashtra said: O Sanjay, after gathering on the holy field of Kurukshetra, and desiring to fight, what did my sons and the sons of Pandu do?',

    'अत्र शूरा महेष्वासा भीमार्जुनसमा युधि':'Behold in their ranks are many powerful warriors, like Yuyudhan, Virat, and Drupad, wielding mighty bows and equal in military prowess to Bheem and Arjun. There are also accomplished heroes like Dhrishtaketu, Chekitan, the gallant King of Kashi, Purujit, Kuntibhoj, and Shaibya—all the best of men. In their ranks, they also have the courageous Yudhamanyu, the gallant Uttamauja, the son of Subhadra, and the sons of Draupadi, who are all great warrior chiefs.',

    'अस्माकं तु विशिष्टा ये तान्निबोध द्विजोत्तम |नायका मम सैन्यस्य संज्ञार्थं तान्ब्रवीमि ते ||':'O best of Brahmins, hear too about the principal generals on our side, who are especially qualified to lead. These I now recount unto you.',

    'भवान्भीष्मश्च कर्णश्च कृपश्च समितिञ्जय: |अश्वत्थामा विकर्णश्च सौमदत्तिस्तथैव च ||':'There are personalities like yourself, Bheeshma, Karna, Kripa, Ashwatthama, Vikarn, and Bhurishrava, who are ever victorious in battle.',

    'अन्ये च बहव: शूरा मदर्थे त्यक्तजीविता: |':'Also, there are many other heroic warriors, who are prepared to lay down their lives for my sake. They are all skilled in the art of warfare, and equipped with various kinds of weapons.',

    'अपर्याप्तं तदस्माकं बलं भीष्माभिरक्षितम् |':'The strength of our army is unlimited and we are safely marshalled by Grandsire Bheeshma, while the strength of the Pandava army, carefully marshalled by Bheem, is limited.',

    'अयनेषु च सर्वेषु यथाभागमवस्थिता: |भीष्ममेवाभिरक्षन्तु भवन्त: सर्व एव हि ||':'Therefore, I call upon all the generals of the Kaurava army now to give full support to Grandsire Bheeshma, even as you defend your respective strategic points.',

    'तस्य सञ्जनयन्हर्षं कुरुवृद्ध: पितामह: |सिंहनादं विनद्योच्चै: शङ्खं दध्मौ प्रतापवान् ||':'Then, the grand old man of the Kuru dynasty, the glorious patriarch Bheeshma, roared like a lion, and blew his conch shell very loudly, giving joy to Duryodhan.',

    'तत: शङ्खाश्च भेर्यश्च पणवानकगोमुखा: |सहसैवाभ्यहन्यन्त स शब्दस्तुमुलोऽभवत् ||':'Thereafter, conches, kettledrums, bugles, trumpets, and horns suddenly blared forth, and their combined sound was overwhelming.',

    'तत: श्वेतैर्हयैर्युक्ते महति स्यन्दने स्थितौ |माधव: पाण्डवश्चैव दिव्यौ शङ्खौ प्रदध्मतु: ||':'Then, from amidst the Pandava army, seated in a glorious chariot drawn by white horses, Madhav and Arjun blew their Divine conch shells.',

    'पाञ्चजन्यं हृषीकेशो देवदत्तं धनञ्जय: |पौण्ड्रं दध्मौ महाशङ्खं भीमकर्मा वृकोदर: ||':'Hrishikesh blew his conch shell, called Panchajanya, and Arjun blew the Devadutta. Bheem, the voracious eater and performer of herculean tasks, blew his mighty conch, called Paundra.',

    'यद्यप्येते न पश्यन्ति लोभोपहतचेतस: |कुलक्षयकृतं दोषं मित्रद्रोहे च पातकम् || कथं न ज्ञेयमस्माभि: पापादस्मान्निवर्तितुम् |कुलक्षयकृतं दोषं प्रपश्यद्भिर्जनार्दन ||':'Their thoughts are overpowered by greed and they see no wrong in annihilating their relatives or wreaking treachery upon friends. Yet, O Janardan (Krishna), why should we, who can clearly see the crime in killing our kindred, not turn away from this sin?',

    'कुलक्षये प्रणश्यन्ति कुलधर्मा: सनातना: |धर्मे नष्टे कुलं कृत्स्नमधर्मोऽभिभवत्युत ||':'When a dynasty is destroyed, its traditions get vanquished, and the rest of the family becomes involved in irreligion.',

    'अधर्माभिभवात्कृष्ण प्रदुष्यन्ति कुलस्त्रिय: |स्त्रीषु दुष्टासु वार्ष्णेय जायते वर्णसङ्कर: ||':'With the preponderance of vice, O Krishna, the women of the family become immoral; and from the immorality of women, O descendent of Vrishni, unwanted progeny are born.',

    'सङ्करो नरकायैव कुलघ्नानां कुलस्य च |पतन्ति पितरो ह्येषां लुप्तपिण्डोदकक्रिया: ||':'An increase in unwanted children results in hellish life both for the family and for those who destroy the family. Deprived of the sacrificial offerings, the ancestors of such corrupt families also fall.',

    'दोषैरेतै: कुलघ्नानां वर्णसङ्करकारकै: |उत्साद्यन्ते जातिधर्मा: कुलधर्माश्च शाश्वता: ||':'Through the evil deeds of those who destroy the family tradition and thus give rise to unwanted progeny, a variety of social and family welfare activities are ruined.',

    'उत्सन्नकुलधर्माणां मनुष्याणां जनार्दन |नरकेऽनियतं वासो भवतीत्यनुशुश्रुम ||':'O Janardan (Krishna), I have heard from the learned that those who destroy family traditions dwell in hell for an indefinite period of time.',

    'अहो बत महत्पापं कर्तुं व्यवसिता वयम् |यद्राज्यसुखलोभेन हन्तुं स्वजनमुद्यता: || यदि मामप्रतीकारमशस्त्रं शस्त्रपाणय: |धार्तराष्ट्रा रणे हन्युस्तन्मे क्षेमतरं भवेत् ||':'Alas! How strange it is that we have set our mind to perform this great sin. Driven by the desire for kingly pleasures, we are intent on killing our own kinsmen. It will be better if, with weapons in hand, the sons of Dhritarashtra kill me unarmed and unresisting on the battlefield.',

    'सञ्जय उवाच |तं तथा कृपयाविष्टमश्रुपूर्णाकुलेक्षणम् |विषीदन्तमिदं वाक्यमुवाच मधुसूदन: ||':'Sanjay said: Seeing Arjun overwhelmed with pity, his mind grief-stricken, and his eyes full of tears, Shree Krishna spoke the following words.',

    'श्रीभगवानुवाच |कुतस्त्वा कश्मलमिदं विषमे समुपस्थितम् |अनार्यजुष्टमस्वर्ग्यमकीर्तिकरमर्जुन ||':'The Supreme Lord said: My dear Arjun, how has this delusion overcome you in this hour of peril? It is not befitting an honorable person. It leads not to the higher abodes, but to disgrace.',

    'क्लैब्यं मा स्म गम: पार्थ नैतत्तवय्युपपद्यते |क्षुद्रं हृदयदौर्बल्यं त्यक्त्वोत्तिष्ठ परन्तप ||':'O Parth, it does not befit you to yield to this unmanliness. Give up such petty weakness of heart and arise, O vanquisher of enemies.',

    'अर्जुन उवाच |कथं भीष्ममहं सङ्ख्ये द्रोणं च मधुसूदन |इषुभि: प्रतियोत्स्यामि पूजार्हावरिसूदन ||':'Arjun said: O Madhusudan, how can I shoot arrows in battle on men like Bheeshma and Dronacharya, who are worthy of my worship, O destroyer of enemies?',

    'गुरूनहत्वा हि महानुभावान्श्रेयो भोक्तुं भैक्ष्यमपीह लोके |हत्वार्थकामांस्तु गुरूनिहैवभुञ्जीय भोगान् रुधिरप्रदिग्धान् ||':'It would be better to live in this world by begging, than to enjoy life by killing these noble elders, who are my teachers. If we kill them, the wealth and pleasures we enjoy will be tainted with blood.',

    'न चैतद्विद्म: कतरन्नो गरीयोयद्वा जयेम यदि वा नो जयेयु: |यानेव हत्वा न जिजीविषामस्तेऽवस्थिता: प्रमुखे धार्तराष्ट्रा: ||':'We do not even know which result of this war is preferable for us—conquering them or being conquered by them. Even after killing them we will not desire to live. Yet they have taken the side of Dhritarasthra, and now stand before us on the battlefield.',

    'कार्पण्यदोषोपहतस्वभाव: पृच्छामि त्वां धर्मसम्मूढचेता: |यच्छ्रेय: स्यान्निश्चितं ब्रूहि तन्मेशिष्यस्तेऽहं शाधि मां त्वां प्रपन्नम् ||':'I am confused about my duty, and am besieged with anxiety and faintheartedness. I am your disciple, and am surrendered to you. Please instruct me for certain what is best for me.',

    'न हि प्रपश्यामि ममापनुद्याद्यच्छोकमुच्छोषणमिन्द्रियाणाम् |अवाप्य भूमावसपत्नमृद्धंराज्यं सुराणामपि चाधिपत्यम् ||':'I can find no means of driving away this anguish that is drying up my senses. Even if I win a prosperous and unrivalled kingdom on the earth, or gain sovereignty like the celestial gods, I will be unable to dispel this grief.',

    'सञ्जय उवाच |एवमुक्त्वा हृषीकेशं गुडाकेश: परन्तप |न योत्स्य इति गोविन्दमुक्त्वा तूष्णीं बभूव ह ||':'Sanjay said: Having thus spoken, Gudakesh, that chastiser of enemies, addressed Hrishikesh: “Govind, I shall not fight,” and became silent.',

    'तमुवाच हृषीकेश: प्रहसन्निव भारत |सेनयोरुभयोर्मध्ये विषीदन्तमिदं वच: ||':'O Dhritarashtra, thereafter, in the midst of both the armies, Shree Krishna smilingly spoke the following words to the grief-stricken Arjun.',

    'श्रीभगवानुवाच |अशोच्यानन्वशोचस्त्वं प्रज्ञावादांश्च भाषसे |गतासूनगतासूंश्च नानुशोचन्ति पण्डिता: ||':'The Supreme Lord said: While you speak words of wisdom, you are mourning for that which is not worthy of grief. The wise lament neither for the living nor for the dead.',

    'न त्वेवाहं जातु नासं न त्वं नेमे जनाधिपा |न चैव न भविष्याम: सर्वे वयमत: परम् ||':'Never was there a time when I did not exist, nor you, nor all these kings; nor in the future shall any of us cease to be.'
}

def sanskrit_to_english(sanskrit_sentence):
    translated_sentence = sanskrit_to_english_dict.get(sanskrit_sentence, None)
    if translated_sentence is None:
        return "Translation not found in the dictionary."
    return translated_sentence

def direct_sanskrit_to_english(sanskrit_paragraph):
    translator = Translator()
    try:
        translated_paragraph = translator.translate(sanskrit_paragraph, src='sa', dest='en')
        return translated_paragraph.text
    except Exception as e:
        print(f"Error with translation API: {e}")
        return "Translation error occurred."

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    sanskrit_text = data.get('sanskritText')

    # Use dictionary translation first, fallback to Google Translate
    translated_text = sanskrit_to_english(sanskrit_text)
    if translated_text == "Translation not found in the dictionary.":
        translated_text = direct_sanskrit_to_english(sanskrit_text)

    return jsonify({'translatedText': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
