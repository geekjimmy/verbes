import json
import sys
import xml.etree.ElementTree as ET

MOODS_FR = {
    'indicative': 'indicatif',
    'conditional': 'conditionnel',
    'subjunctive': 'subjonctif',
    'imperative': 'impératif'
}

TENSES_FR = {
    'present': 'présent',
    'imperfect': 'imparfait',
    'future': 'futur simple',
    'simple-past': 'passé simple',
    'imperative-present': 'présent'
}

MOODS = {
    # 'infinitive': ['infinitive-present'],
    'indicative': ['present', 'imperfect', 'future', 'simple-past'],
    'conditional': ['present'],
    'subjunctive': ['present'],
    'imperative': ['imperative-present'],
    # 'participle': ['present-participle', 'past-participle']
}

def xml_to_dict(template):
    d = {}
    for mood_name, tenses in MOODS.items():
        d[mood_name] = {}
        t = template.find(mood_name)
        for tense_name in tenses:
            s = t.find(tense_name)
            tense = d[mood_name][tense_name] = []
            for p in s.findall('p'):
                tmp = []
                for i in p.findall('i'):
                    tmp.append(i.text if i.text is not None else '')
                tense.append(tmp)
    return d

class Verb:
    def __init__(self, infinitive, conjugation, root):
        self.infinitive = infinitive
        self.conjugation = conjugation
        self.root = root

def persons(tense):
    if tense == 'imperative-present':
        return [('s', 2), ('p', 1), ('p', 2)]

    return [('s', 1), ('s', 2), ('s', 3),
            ('p', 1), ('p', 2), ('p', 3)]

def main():
    tree = ET.parse(sys.argv[1])
    verbs_root = tree.getroot()

    tree = ET.parse(sys.argv[2])
    templates_root = tree.getroot()

    white_list = set()
    if len(sys.argv) == 4:
        with open(sys.argv[3]) as verbs:
            for verb in verbs:
                white_list.add(verb.strip())

    templates = {}

    verbs = []

    for template in templates_root:
        templates[template.attrib['name']] = xml_to_dict(template)

    for verb in verbs_root:
        infinitive = verb.find('i').text
        if not infinitive in white_list:
            continue

        template = verb.find('t').text
        conjugation = templates[template]
        length_after_colon = len(template) - template.find(':')
        root = infinitive[:-length_after_colon + 1]
        verbs.append(Verb(infinitive, conjugation, root))

    fixture = []

    for verb in sorted(verbs, key=lambda v: v.infinitive):
        fixture.append({
            'pk': None,
            'model': 'app.Verb',
            'fields': {
                'name': verb.infinitive
            }
        })
        for mood, tenses in sorted(verb.conjugation.items(), key=lambda c: c[0]):
            for tense, conjugations in sorted(tenses.items(), key=lambda t: t[0]):
                for person, conj in zip(persons(tense), conjugations):
                    if len(conj) == 0:
                        continue

                    fixture.append({
                        'pk': None,
                        'model': 'app.Conjugation',
                        'fields': {
                            'verb': [verb.infinitive],
                            'mood_tense': [MOODS_FR[mood], TENSES_FR[tense]],
                            'person': [person[0], person[1]]
                        }
                    })

                    for c in sorted(conj):
                        fixture.append({
                            'pk': None,
                            'model': 'app.ConjugationValue',
                            'fields': {
                                'conjugation': [verb.infinitive, MOODS_FR[mood], TENSES_FR[tense], person[0], person[1]],
                                'value': verb.root + c
                            }
                        })

    print(json.dumps(fixture, indent=2, ensure_ascii=False, sort_keys=True))



if __name__ == '__main__':
    main()
