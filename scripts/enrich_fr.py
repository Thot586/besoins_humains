import pathlib

EDITS_FR = [
    ('besoins/affection.html',
     "Recevoir l'amour se pratique, autant que le donner — souvent c'est même le plus difficile.</li>",
     "Recevoir l'amour se pratique, autant que le donner — souvent c'est même le plus difficile <em>(par&nbsp;ex. accueillir un compliment sans le minimiser, ou laisser un proche nous aider sans aussitôt chercher à rembourser)</em>.</li>"),
    ('besoins/affection.html',
     'qu\'on voit beaucoup de monde.<a class="ref-anchor"',
     'qu\'on voit beaucoup de monde <em>(par&nbsp;ex. rentrer d\'une soirée animée avec une sensation d\'absence intérieure)</em>.<a class="ref-anchor"'),
    ('besoins/affection.html',
     "écrans partout, attention sans cesse coupée.</li>",
     "écrans partout, attention sans cesse coupée <em>(par&nbsp;ex. poser le téléphone dans une autre pièce pendant une visite)</em>.</li>"),

    ('besoins/comprehension.html',
     'Tout remettre à plus tard</strong>, ne plus arriver à décider.<a class="ref-anchor"',
     'Tout remettre à plus tard</strong>, ne plus arriver à décider <em>(par&nbsp;ex. faire défiler les formations en ligne pendant des semaines sans jamais en choisir une)</em>.<a class="ref-anchor"'),
    ('besoins/comprehension.html',
     'Cette zone juste est étroite et change avec le temps.<a class="ref-anchor"',
     'Cette zone juste est étroite et change avec le temps <em>(par&nbsp;ex. apprendre un morceau légèrement au-dessus de son niveau, pas le morceau virtuose qui fait abandonner dès la première mesure)</em>.<a class="ref-anchor"'),
    ('besoins/comprehension.html',
     "Croire qu'il faut attendre la motivation pour commencer. La motivation vient plutôt dans l'action, rarement avant.</li>",
     "Croire qu'il faut attendre la motivation pour commencer <em>(par&nbsp;ex. se dire « je m'y mets quand je serai prêt », alors que cinq minutes maladroites suffisent à lancer le mouvement)</em>. La motivation vient plutôt dans l'action, rarement avant.</li>"),

    ('besoins/creation.html',
     "Créer vaut la peine même sans talent reconnu — la valeur est dans l'acte, pas dans la manière dont ce sera reçu.</li>",
     "Créer vaut la peine même sans talent reconnu — la valeur est dans l'acte, pas dans la manière dont ce sera reçu <em>(par&nbsp;ex. tenir un carnet qu'on ne montrera à personne, ou improviser au piano sans public)</em>.</li>"),
    ('besoins/creation.html',
     "ennui profond même dans une vie objectivement bien remplie.</li>",
     "ennui profond même dans une vie objectivement bien remplie <em>(par&nbsp;ex. une vie lisse et réussie en apparence, avec l'impression diffuse que « ce n'est pas vraiment soi qui vit ça »)</em>.</li>"),
    ('besoins/creation.html',
     "<strong>métriques extérieures</strong> — likes, ventes, algorithmes.</li>",
     "<strong>métriques extérieures</strong> — likes, ventes, algorithmes <em>(par&nbsp;ex. ne poster une photo que si elle va « bien marcher », au point d'oublier pourquoi on l'avait prise)</em>.</li>"),

    ('besoins/identite.html',
     "surtout après une perte ou après un grand accomplissement.</li>",
     "surtout après une perte ou après un grand accomplissement <em>(par&nbsp;ex. avoir obtenu le poste rêvé et ne plus savoir qui l'on est sans ce projet, ou perdre un proche et sentir disparaître une partie de soi avec)</em>.</li>"),
    ('besoins/identite.html',
     '(venues des parents, de la société). Clarifier ses valeurs est un levier efficace bien étudié.<a class="ref-anchor"',
     '(venues des parents, de la société) <em>(par&nbsp;ex. se demander si « réussir » reste important une fois coupée la voix familiale qui l\'a répété)</em>. Clarifier ses valeurs est un levier efficace bien étudié.<a class="ref-anchor"'),
    ('besoins/identite.html',
     "Achats démonstratifs comme signal de ce qu'on est — on finit par se définir par ce qu'on possède.</li>",
     "Achats démonstratifs comme signal de ce qu'on est — on finit par se définir par ce qu'on possède <em>(par&nbsp;ex. accumuler des marques visibles pour que les autres « devinent » qui l'on est)</em>.</li>"),

    ('besoins/liberte.html',
     "La liberté intérieure se construit à travers de petites décisions répétées, pas par un seul grand saut.</li>",
     "La liberté intérieure se construit à travers de petites décisions répétées, pas par un seul grand saut <em>(par&nbsp;ex. commencer par dire non à un verre qu'on ne veut pas, puis à une réunion qui ne nous concerne pas, puis à un projet qu'on ne choisit pas vraiment)</em>.</li>"),
    ('besoins/liberte.html',
     "<strong>décider seul</strong>, même pour des choix mineurs, sans chercher l'approbation d'un autre.</li>",
     "<strong>décider seul</strong>, même pour des choix mineurs, sans chercher l'approbation d'un autre <em>(par&nbsp;ex. hésiter entre deux plats au restaurant au point de faire le tour de la table pour un avis)</em>.</li>"),
    ('besoins/liberte.html',
     "<strong>décider de plus en plus par soi-même</strong> — commencer par de petites choses.</li>",
     "<strong>décider de plus en plus par soi-même</strong> — commencer par de petites choses <em>(par&nbsp;ex. choisir son week-end sans consulter personne, puis ses prochaines vacances, puis un changement de vie sans attendre la permission)</em>.</li>"),

    ('besoins/loisir.html',
     "<strong>Culpabilité</strong> dès qu'on s'arrête — le repos lui-même devient une performance.</li>",
     "<strong>Culpabilité</strong> dès qu'on s'arrête — le repos lui-même devient une performance <em>(par&nbsp;ex. penser à la liste des tâches dès le dimanche matin au lit, ou « jeter un œil » à ses mails professionnels en vacances)</em>.</li>"),
    ('besoins/loisir.html',
     'au-delà du simple fait d\'en être physiquement absent.<a class="ref-anchor"',
     'au-delà du simple fait d\'en être physiquement absent <em>(par&nbsp;ex. ne pas ouvrir son ordinateur un jour de congé, même « juste cinq minutes »)</em>.<a class="ref-anchor"'),
    ('besoins/loisir.html',
     "<strong>Vacances sur-planifiées</strong> qui n'offrent aucune vraie décompression.</li>",
     "<strong>Vacances sur-planifiées</strong> qui n'offrent aucune vraie décompression <em>(par&nbsp;ex. cocher trois pays en deux semaines avec une to-do des monuments à voir)</em>.</li>"),

    ('besoins/participation.html',
     'Se sentir <strong>inutile</strong> et à la marge, même quand on est entouré.<a class="ref-anchor"',
     'Se sentir <strong>inutile</strong> et à la marge, même quand on est entouré <em>(par&nbsp;ex. avoir l\'impression, au bureau ou en famille, que tout continuerait à tourner pareil sans nous)</em>.<a class="ref-anchor"'),
    ('besoins/participation.html',
     "Choisir un engagement qui correspond à ses <strong>valeurs profondes</strong>, pas n'importe lequel.</li>",
     "Choisir un engagement qui correspond à ses <strong>valeurs profondes</strong>, pas n'importe lequel <em>(par&nbsp;ex. donner du temps à une cause qui nous touche vraiment, plutôt qu'à celle qui est médiatique du moment)</em>.</li>"),
    ('besoins/participation.html',
     "<strong>Appartenance passive</strong> en ligne : consommer sans jamais rien donner en retour.</li>",
     "<strong>Appartenance passive</strong> en ligne : consommer sans jamais rien donner en retour <em>(par&nbsp;ex. être membre de dizaines de groupes en ligne sans y avoir jamais écrit un seul message)</em>.</li>"),

    ('besoins/protection.html',
     "<strong>Se sentir en alerte en permanence</strong>, même quand la situation est objectivement sûre.</li>",
     "<strong>Se sentir en alerte en permanence</strong>, même quand la situation est objectivement sûre <em>(par&nbsp;ex. tressaillir au moindre bruit chez soi, rester « sur le qui-vive » même un dimanche sans rien de prévu)</em>.</li>"),
    ('besoins/protection.html',
     "<strong>routines régulières</strong> (heures, lieux, gestes) qui créent une sécurité de base à l'intérieur.</li>",
     "<strong>routines régulières</strong> (heures, lieux, gestes) qui créent une sécurité de base à l'intérieur <em>(par&nbsp;ex. un même réveil, un même petit-déjeuner, un même trajet le matin)</em>.</li>"),
    ('besoins/protection.html',
     "Accepter de <strong>demander, recevoir, s'appuyer</strong> sur les autres quand on en a besoin — c'est un signe de maturité, pas de faiblesse.</li>",
     "Accepter de <strong>demander, recevoir, s'appuyer</strong> sur les autres quand on en a besoin — c'est un signe de maturité, pas de faiblesse <em>(par&nbsp;ex. laisser un proche porter un carton au déménagement, ou admettre qu'on a besoin d'aide professionnelle sans le vivre comme une défaite)</em>.</li>"),

    ('besoins/subsistance.html',
     "<strong>Fatigue qui dure</strong>, que le repos ne suffit pas à enlever.</li>",
     "<strong>Fatigue qui dure</strong>, que le repos ne suffit pas à enlever <em>(par&nbsp;ex. dormir douze heures un samedi et se réveiller aussi vidé qu'avant)</em>.</li>"),
    ('besoins/subsistance.html',
     "Surveiller en permanence ses données (pas, sommeil, fréquence cardiaque) comme un tableau de bord. Le corps devient un objet à optimiser, la vie s'éloigne.</li>",
     "Surveiller en permanence ses données (pas, sommeil, fréquence cardiaque) comme un tableau de bord <em>(par&nbsp;ex. consulter dix fois par jour ses statistiques de pas ou de sommeil, jusqu'à ce que la mesure remplace le ressenti)</em>. Le corps devient un objet à optimiser, la vie s'éloigne.</li>"),
]

miss, ok = 0, 0
for path, old, new in EDITS_FR:
    p = pathlib.Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        print(f'MISS: {path} :: {old[:70]}')
        miss += 1
        continue
    p.write_text(text.replace(old, new, 1), encoding='utf-8')
    ok += 1
    print(f'OK:   {path} :: {old[:70]}')

print(f'\n{ok} applied, {miss} missed')
