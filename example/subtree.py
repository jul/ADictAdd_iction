# coding: utf-8
import json

from vector_dict.VectorDict import convert_tree

big_dict = json.loads('''
{
  "city": {
    "geoname_id": 4709796,
    "names": {
      "ru": "Мак-Аллен",
      "en": "McAllen",
      "pt-BR": "McAllen",
      "ja": "マッカレン",
      "zh-CN": "麦卡伦"
    }
  },
  "country": {
    "geoname_id": 6252001,
    "iso_code": "US",
    "names": {
      "ru": "США",
      "fr": "États-Unis",
      "en": "United States",
      "de": "USA",
      "zh-CN": "美国",
      "pt-BR": "Estados Unidos",
      "ja": "アメリカ合衆国",
      "es": "Estados Unidos"
    }
  },
  "registered_country": {
    "geoname_id": 6252001,
    "iso_code": "US",
    "names": {
      "ru": "США",
      "fr": "États-Unis",
      "en": "United States",
      "de": "USA",
      "zh-CN": "美国",
      "pt-BR": "Estados Unidos",
      "ja": "アメリカ合衆国",
      "es": "Estados Unidos"
    }
  },
  "subdivisions": [
    {
      "geoname_id": 4736286,
      "iso_code": "TX",
      "names": {
        "ru": "Техас",
        "en": "Texas",
        "ja": "テキサス州",
        "es": "Texas",
        "zh-CN": "得克萨斯州"
      }
    }
  ],
  "location": {
    "latitude": 26.2759,
    "time_zone": "America/Chicago",
    "longitude": -98.233,
    "metro_code": "636"
  },
  "postal": {
    "code": "78504"
  },
  "continent": {
    "geoname_id": 6255149,
    "code": "NA",
    "names": {
      "ru": "Северная Америка",
      "fr": "Amérique du Nord",
      "en": "North America",
      "de": "Nordamerika",
      "zh-CN": "北美洲",
      "pt-BR": "América do Norte",
      "ja": "北アメリカ",
      "es": "Norteamérica"
    }
  }
}''')

tmpl_dict = json.loads('''
{
  "city": {
    "names": {
      "en": ""
    }
  },
  "country": {
    "iso_code": ""
  },
  "location": {
    "time_zone": ""
  },
  "postal": {
    "code": ""
  }
}''')

big_tree = convert_tree(big_dict)
tmpl_tree = convert_tree(tmpl_dict)

big_tree.intersection(tmpl_tree, ignore_value_difference=True).tprint()

"""
{
    u'city' : {
        u'names' : {
            u'en' : 'McAllen',
        },
    },
    u'postal' : {
        u'code' : '78504',
    },
    u'location' : {
        u'time_zone' : 'America/Chicago',
    },
    u'country' : {
        u'iso_code' : 'US',
    },
}
"""
