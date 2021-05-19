from django.test import TestCase

import json
from pprint import pprint
import os

from .eurovision_youtube_counter.src import db_connect as db
#from eurovision_data.video_data.services.video_json_connect import get_video_urls
from .eurovision_youtube_counter.src.youtube_connector import YoutubeConnect
from django.conf import settings


class JsonTests(TestCase):

    def test_open_json_file(self):
        file_path = os.path.join(os.path.abspath(''), r'video_data/eurovision_youtube_counter/videos.json')

        with open(file_path) as f:
            data = json.load(f)
        pprint(data)

    def test_read_json_file(self):
        file_path = os.path.join(os.path.abspath(''), r'video_data/eurovision_youtube_counter/videos.json')

        with open(file_path) as f:
            data = json.load(f)

        print(data['video_group'][0]['videos'][0]['link'])

        for x in data['video_group']:
            print(x['type'])

    def test_read_json_result_file(self):
        file_path = os.path.join(os.path.abspath(''), r'video_data/eurovision_youtube_counter/eurocontests_results.json')

        with open(file_path) as f:
            data = json.load(f)
        country_list = []
        for period in data['eurovision_final_results']:
            year = period['year']
            print(f'year: {year}')
            for country in period['countries']:
                print(country)
                #print('country: ' + country['country_name'])
                #print('jury_ranking: ' + country['jury_ranking'])
                #print('tele_ranking: ' + country['tele_ranking'])

#    def test_call_json_connect(self):
#        get_video_urls()


class DatabaseTests(TestCase):

    def test_read_from_db(self):
        print(db.read_data())


class YoutubeTests(TestCase):

    def test_youtube_class_connection(self):
        youtube = YoutubeConnect()
        youtube_video_id = 'clltO-wwfRE'
        part = 'snippet,contentDetails,statistics'
        results = youtube.get_video_data(part, youtube_video_id)
        print(results)


class StringTests(TestCase):

    def test_create_json_string_from_template_for_country_results(self):
        country_list_2017 = ["1, 1, 1, 0, 758, 382, 376, 6, , Portugal, Salvador Sobral, Amar Pelos Dois",
                        "2, 2, 2, 0, 615, 278, 337, 59, , Bulgaria, Kristian Kostov, Beautiful Mess",
                        "3, 8, 3, 5, 374, 110, 264, 154, , Moldova, Sunstroke Project, Hey Mamma",
                        "4, 9, 4, 5, 363, 108, 255, 147, , Belgium, Blanche, City Lights",
                        "5, 3, 8, 5, 344, 218, 126, 92, , Sweden, Robin Bengtsson, I Can't Go On",
                        "6, 7, 6, 1, 334, 126, 208, 82, , Italy, Francesco Gabbani, Occidentali's Karma",
                        "7, 14, 5, 9, 282, 58, 224, 166, , Romania, Ilinca ft. Alex Florea, Yodel It!",
                        "8, 17, 7, 10, 200, 48, 152, 104, , Hungary, Joci Pápai, Origo",
                        "9, 4, 25, 21, 173, 171, 2, 169, , Australia, Isaiah, Don't Come Easy",
                        "10, 6, 15, 9, 158, 129, 29, 100, , Norway, JOWST, Grab The Moment",
                        "11, 5, 19, 14, 150, 135, 15, 120, , Netherlands, OG3NE, Lights and Shadows",
                        "12, 19, 10, 9, 135, 45, 90, 45, , France, Alma, Requiem",
                        "13, 22, 9, 13, 128, 25, 103, 78, , Croatia, Jacques Houdek, My Friend",
                        "14, 12, 11, 1, 120, 78, 42, 36, , Azerbaijan, Dihaj, Skeletons",
                        "15, 10, 20, 10, 111, 99, 12, 87, , United Kingdom, Lucie Jones, Never Give Up On You",
                        "16, 11, 26, 15, 93, 93, 0, 93, , Austria, Nathan Trent, Running On Air",
                        "17, 16, 13, 3, 83, 50, 33, 17, , Belarus, Naviband, Story of My Life",
                        "18, 14, 18, 4, 79, 58, 21, 37, , Armenia, Artsvik, Fly With Me",
                        "19, 17, 15, 2, 77, 48, 29, 19, , Greece, Demy, This is Love",
                        "20, 13, 21, 8, 77, 69, 8, 61, , Denmark, Anja, Where I Am",
                        "21, 20, 14, 6, 68, 36, 32, 4, , Cyprus, Hovig, Gravity",
                        "22, 23, 12, 11, 64, 23, 41, 18, , Poland, Kasia Moś, Flashlight",
                        "23, 21, 22, 1, 39, 34, 5, 29, , Israel, IMRI, I Feel Alive",
                        "24, 24, 17, 7, 36, 12, 24, 12, , Ukraine, O.Torvald, Time",
                        "25, 25, 24, 1, 6, 3, 3, 0, , Germany, Levina, Perfect Life",
                        "26, 26, 22, 4, 5, 0, 5, 5, , Spain, Manel Navarro, Do It For Your Lover"]

        country_list_2018 = ["1, 3, 1, 2, 529, 212, 317, 105, , Israel, Netta, TOY",
                            "2, 5, 2, 3, 436, 183, 253, 70, , Cyprus, Eleni Foureira, Fuego",
                            "3, 1, 13, 12, 342, 271, 71, 200, , Austria, Cesár Sampson, Nobody But You",
                            "4, 4, 6, 2, 340, 204, 136, 68, , Germany, Michael Schulte, You Let Me Walk Alone",
                            "5, 17, 3, 14, 308, 59, 249, 190, , Italy, Ermal Meta e Fabrizio Moro, Non Mi Avete Fatto Niente",
                            "6, 15, 4, 11, 281, 66, 215, 149, , Czech Republic, Mikolas Josef, Lie To Me",
                            "7, 2, 23, 21, 274, 253, 21, 232, , Sweden, Benjamin Ingrosso, Dance You Off",
                            "8, 6, 9, 3, 245, 143, 102, 41, , Estonia, Elina Nechayeva, La Forza",
                            "9, 21, 5, 16, 226, 38, 188, 150, , Denmark, Rasmussen, Higher Ground",
                            "10, 10, 8, 2, 209, 94, 115, 21, , Moldova, DoReDos, My Lucky Day",
                            "11, 7, 18, 11, 184, 126, 58, 68, , Albania, Eugent Bushpepa, Mall",
                            "12, 11, 10, 1, 181, 90, 91, 1, , Lithuania, Ieva Zasimauskaitė, When We're Old",
                            "13, 8, 17, 9, 173, 114, 59, 55, , France, Madame Monsieur, Mercy",
                            "14, 9, 14, 5, 166, 100, 66, 34, , Bulgaria, EQUINOX, Bones",
                            "15, 16, 11, 5, 144, 60, 84, 24, , Norway, Alexander Rybak, That's How You Write A Song",
                            "16, 14, 16, 2, 136, 74, 62, 12, , Ireland, Ryan O'Shaughnessy, Together",
                            "17, 26, 7, 19, 130, 11, 119, 108, , Ukraine, MELOVIN, Under The Ladder",
                            "18, 13, 19, 6, 121, 89, 32, 57, , Netherlands, Waylon, Outlaw In 'Em",
                            "19, 20, 12, 8, 113, 38, 75, 37, , Serbia, Sanja Ilić & Balkanika, Nova Deca",
                            "20, 12, 26, 14, 99, 90, 9, 81, , Australia, Jessica Mauboy, We Got Love",
                            "21, 22, 15, 7, 93, 28, 65, 37, , Hungary, AWS, Viszlát Nyár",
                            "22, 19, 22, 3, 64, 41, 23, 18, , Slovenia, Lea Sirk, Hvala, ne!",
                            "23, 18, 24, 6, 61, 43, 18, 25, , Spain, Amaia y Alfred, Tu Canción",
                            "24, 23, 20, 3, 48, 23, 25, 2, , United Kingdom, SuRie, Storm",
                            "25, 24, 21, 3, 46, 23, 23, 0, , Finland, Saara Aalto, Monsters",
                            "26, 25, 25, 0, 39, 21, 18, 3, , Portugal, Cláudia Pascoal, O Jardim"]

        country_list_2019 = ["1, 3, 2, 1, 498, 237, 261, 24, , Netherlands, Duncan Laurence, Arcade",
                            "2, 4, 3, 1, 472, 219, 253, 34, , Italy, Mahmood, Soldi",
                            "3, 9, 4, 5, 370, 126, 244, 118, , Russia, Sergey Lazarev, Scream",
                            "4, 7, 5, 2, 364, 152, 212, 60, , Switzerland, Luca Hänni, She Got Me",
                            "5, 2, 9, 7, 334, 241, 93, 148, , Sweden, John Lundvik, Too Late For Love",
                            "6, 18, 1, 17, 331, 40, 291, 251, , Norway, KEiiNO, Spirit in the Sky",
                            "7, 1, 12, 11, 305, 247, 58, 189, , North Macedonia, Tamara Todevska, Proud",
                            "8, 5, 8, 3, 302, 202, 100, 102, , Azerbaijan, Chingiz, Truth",
                            "9, 6, 7, 1, 284, 153, 131, 22, , Australia, Kate Miller-Heidke, Zero Gravity",
                            "10, 16, 6, 10, 232, 46, 186, 140, , Iceland, Hatari, Hatrið mun sigra",
                            "11, 8, 24, 16, 157, 150, 7, 143, , Czech Republic, Lake Malawi, Friend of a Friend",
                            "12, 12, 15, 3, 120, 69, 51, 18, , Denmark, Leonora, Love Is Forever",
                            "13, 11, 20, 9, 109, 77, 32, 45, , Cyprus, Tamta, Replay",
                            "14, 10, 22, 12, 107, 87, 20, 67, , Malta, Michela, Chameleon",
                            "15, 15, 11, 4, 105, 46, 59, 13, , Slovenia, Zala Kralj & Gašper Šantl, Sebi",
                            "16, 13, 18, 5, 105, 67, 38, 29, , France, Bilal Hassani, Roi",
                            "17, 17, 17, 0, 90, 43, 47, 4, , Albania, Jonida Maliqi, Ktheju tokës",
                            "18, 19, 13, 6, 89, 35, 54, 19, , Serbia, Nevena Božović, Kruna",
                            "19, 23, 10, 13, 77, 12, 65, 53, , San Marino, Serhat, Say Na Na Na",
                            "20, 20, 16, 4, 76, 28, 48, 20, , Estonia, Victor Crone, Storm",
                            "21, 14, 21, 7, 74, 50, 24, 26, , Greece, Katerine Duska, Better Love",
                            "22, 25, 14, 11, 54, 1, 53, 52, , Spain, Miki, La Venda",
                            "23, 26, 19, 7, 35, 0, 35, 35, , Israel, Kobi Marimi, Home",
                            "24, 22, 23, 1, 31, 18, 13, 5, , Belarus, ZENA, Like It",
                            "25, 21, 26, 5, 24, 24, 0, 24, , Germany, S!sters, Sister",
                            "26, 24, 25, 1, 11, 8, 3, 5, , United Kingdom, Michael Rice, Bigger Than Us"]

        json_string = ''
        json_string += '{\n'
        json_string += '"eurovision_final_results": [\n'
        json_string += '{\n'
        json_string += '"year": "2017",\n'
        json_string += '"countries": [\n'
        for country_result in country_list_2017:
            result_list = country_result.split(',')

            json_string += '{\n'
            json_string += '"country_name": "' + result_list[9].strip() + '",\n'
            json_string += '"song_name": "' + result_list[11].strip() + '",\n'
            json_string += '"artist_name": "' + result_list[10].strip() + '",\n'
            json_string += '"jury_points": "' + result_list[5].strip() + '",\n'
            json_string += '"tele_points": "' + result_list[6].strip() + '",\n'
            json_string += '"total_points": "' + result_list[4].strip() + '",\n'
            json_string += '"jury_ranking": "' + result_list[1].strip() + '",\n'
            json_string += '"tele_ranking": "' + result_list[2].strip() + '",\n'
            json_string += '"total_ranking": "' + result_list[0].strip() + '"\n'

            json_string += '},\n'

        json_string = json_string[:-2] + '\n'
        json_string += ']\n'
        json_string += '},\n'
        json_string += '{\n'
        json_string += '"year": "2018",\n'
        json_string += '"countries": [\n'
        for country_result in country_list_2018:
            result_list = country_result.split(',')

            json_string += '{\n'
            json_string += '"country_name": "' + result_list[9].strip() + '",\n'
            json_string += '"song_name": "' + result_list[11].strip() + '",\n'
            json_string += '"artist_name": "' + result_list[10].strip() + '",\n'
            json_string += '"jury_points": "' + result_list[5].strip() + '",\n'
            json_string += '"tele_points": "' + result_list[6].strip() + '",\n'
            json_string += '"total_points": "' + result_list[4].strip() + '",\n'
            json_string += '"jury_ranking": "' + result_list[1].strip() + '",\n'
            json_string += '"tele_ranking": "' + result_list[2].strip() + '",\n'
            json_string += '"total_ranking": "' + result_list[0].strip() + '"\n'

            json_string += '},\n'

        json_string = json_string[:-2] + '\n'
        json_string += ']\n'
        json_string += '},\n'

        json_string += '{\n'
        json_string += '"year": "2019",\n'
        json_string += '"countries": [\n'
        for country_result in country_list_2019:
            result_list = country_result.split(',')

            json_string += '{\n'
            json_string += '"country_name": "' + result_list[9].strip() + '",\n'
            json_string += '"song_name": "' + result_list[11].strip() + '",\n'
            json_string += '"artist_name": "' + result_list[10].strip() + '",\n'
            json_string += '"jury_points": "' + result_list[5].strip() + '",\n'
            json_string += '"tele_points": "' + result_list[6].strip() + '",\n'
            json_string += '"total_points": "' + result_list[4].strip() + '",\n'
            json_string += '"jury_ranking": "' + result_list[1].strip() + '",\n'
            json_string += '"tele_ranking": "' + result_list[2].strip() + '",\n'
            json_string += '"total_ranking": "' + result_list[0].strip() + '"\n'

            json_string += '},\n'

        json_string = json_string[:-2] + '\n'
        json_string += ']\n'
        json_string += '}\n'

        json_string += ']\n'
        json_string += '}\n'
        #print(json_string)
        #json_string = json_string.replace('\'', r'\'')
        print(json_string)
        json_obj = json.loads(json_string)
        print(json.dumps(json_obj))
        #pprint(json_obj)
