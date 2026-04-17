"""Remplacer le bloc pseudo-satisfacteur générique par une version
spécifique au besoin de la page."""
import pathlib
import re

BLOCKS_FR = {
    'affection': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : les centaines de contacts en ligne qui ne remplacent pas un lien profond, l'attachement à une cause abstraite ou à une figure admirée de loin. Le vide relationnel revient plus fort après — c'est le signal.",
    'comprehension': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : collectionner les diplômes sans pratiquer, regarder passivement des vidéos d'experts sans jamais s'y mettre soi-même. On se sent cultivé mais on n'a rien appris à faire — le vrai manque revient.",
    'creation': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : poster pour les likes plutôt que pour le geste, attendre l'inspiration au lieu de créer, viser la performance au lieu du plaisir. Le geste créatif se dessèche pendant qu'on optimise sa réception.",
    'identite': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : signaler qui on est par des achats démonstratifs, par les applaudissements, par l'adhésion à une idéologie rigide. On se définit de l'extérieur ; le vide de soi revient dès que le miroir social s'éteint.",
    'liberte': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : le consumérisme qui déguise l'absence de vrai choix en choix entre vingt marques, le refus systématique de tout engagement, la révolte sans projet. Ce qui imite la liberté reproduit souvent la dépendance.",
    'loisir': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : scroller en continu, enchaîner alcool et écrans pour décrocher, planifier chaque minute de ses vacances. On « fait quelque chose » sans vraiment se reposer — la fatigue revient plus lourde.",
    'participation': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : appartenir passivement à des communautés en ligne sans jamais contribuer, rejoindre une idéologie rigide pour y trouver sa place, critiquer en permanence sans agir. On cherche le lien collectif, on obtient l'isolement en groupe.",
    'protection': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : accumuler des biens pour se rassurer, s'isoler « par précaution », tout contrôler chez ses proches, se plonger dans le travail pour fuir l'angoisse. La sécurité extérieure masque pour un temps l'insécurité intérieure — qui revient.",
    'subsistance': "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Ici : empiler les compléments alimentaires, enchaîner les régimes, tracker chaque pas et chaque battement de cœur. Le corps devient un tableau de bord à optimiser — l'attention à ce qu'il ressent vraiment s'éteint.",
}

BLOCKS_EN = {
    'affection': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: hundreds of online contacts that don't replace a deep bond, attachment to an abstract cause or a figure admired from afar. The relational emptiness returns stronger afterward — that's the signal.",
    'understanding': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: collecting diplomas without practising, passively watching expert videos without ever trying yourself. You feel cultured but you haven't learned to do anything — the real lack returns.",
    'creation': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: posting for likes rather than for the act, waiting for inspiration instead of creating, aiming at performance instead of pleasure. The creative gesture dries up while you optimise its reception.",
    'identity': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: signalling who you are through showy purchases, through applause, through adherence to a rigid ideology. You define yourself from the outside; the emptiness inside returns the moment the social mirror turns off.",
    'freedom': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: consumerism that dresses up the lack of real choice as choosing among twenty brands, systematic refusal of any commitment, rebellion without a project. What mimics freedom often reproduces dependence.",
    'leisure': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: endless scrolling, alcohol and screens to switch off, over-planning every minute of a holiday. You are \"doing something\" without actually resting — tiredness comes back heavier.",
    'participation': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: passively belonging to online communities without ever contributing, joining a rigid ideology to find your place, constantly criticising without acting. You look for collective connection and end up isolated within a group.",
    'protection': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: piling up possessions to feel safe, isolating \"just in case\", controlling those close to you, plunging into work to escape anxiety. Outer safety masks, for a while, inner insecurity — which returns.",
    'subsistence': "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Here: piling up supplements, moving from diet to diet, tracking every step and heartbeat. The body becomes a dashboard to optimise — attention to what it actually feels fades out.",
}

# Generic paragraph to replace (exact current text)
GENERIC_FR = "Max-Neef appelle <strong>pseudo-satisfacteur</strong> ce qui promet de combler un besoin mais le creuse en réalité. Exemples&nbsp;: la consommation compulsive pour l'identité, le scrolling infini pour la participation, l'accumulation de diplômes pour la compréhension. La sensation de manque revient plus fort après coup — c'est le signal."

GENERIC_EN = "Max-Neef calls a <strong>pseudo-satisfier</strong> anything that promises to meet a need but actually deepens the lack. Examples: compulsive consumption for identity, endless scrolling for participation, collecting diplomas for understanding. The sense of lack returns stronger afterward — that's the signal."

def run():
    ok = miss = 0
    for slug, new_p in BLOCKS_FR.items():
        path = pathlib.Path(f'besoins/{slug}.html')
        t = path.read_text(encoding='utf-8')
        if GENERIC_FR not in t:
            print(f'MISS: {path}')
            miss += 1
            continue
        path.write_text(t.replace(GENERIC_FR, new_p, 1), encoding='utf-8')
        print(f'OK:   {path}')
        ok += 1
    for slug, new_p in BLOCKS_EN.items():
        path = pathlib.Path(f'en/needs/{slug}.html')
        t = path.read_text(encoding='utf-8')
        if GENERIC_EN not in t:
            print(f'MISS: {path}')
            miss += 1
            continue
        path.write_text(t.replace(GENERIC_EN, new_p, 1), encoding='utf-8')
        print(f'OK:   {path}')
        ok += 1
    print(f'\n{ok} applied, {miss} missed')

if __name__ == '__main__':
    run()
