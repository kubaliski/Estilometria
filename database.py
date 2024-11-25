# database.py
sample_texts = [
    {
        "id": 1,
        "autor": "Autor1",
        "texto": """
        Ayer bine a la escuela y no havia nadie en el salon principal. Me sorprendio mucho porque normalmente
        ay bastante actividad a esa hora. La profesora no yego a tiempo, lo qual es muy raro en ella porque
        siempre es muy puntual. Me parese que todos estavan enfermos o quizas ubo algun problema que no
        me entere. La verdad es que no se que paso ese dia, pero fue muy extraño.

        Despues de esperar casi una hora, decidi irme a la biblioteca para haprobechar el tiempo. Estube
        leyendo un libro muy interesante sobre la istoria antigua. Me hubiera gustado quedarme mas tiempo,
        pero tenia que ir a otra clase. Cuando sali, vi que havia llegado mas jente, pero todavia parecia
        que faltavan muchas personas.

        En la tarde, me encontre con algunos compañeros que me explicaron que hubo una confusion con el
        horario. Havian cambiado la hora de la clase pero no havisaron a todos. Por eso muchos no vinieron
        temprano. Me parecio muy mal que no nos informaran mejor sobre estos cambios. Creo que deverian
        mejorar la comunicasion entre profesores y alumnos.
        """
    },
    {
        "id": 2,
        "autor": "Autor2",
        "texto": """
        El examen de ayer fue mui dificil, mucho mas de lo que esperaba. La maestra no havía explicado
        vien el tema en clase y todos estavamos bastante confundidos. Me parese que nadie paso la prueva,
        o al menos eso es lo que comentavan mis compañeros cuando salimos. Espero que la proxima vez sea
        mas facil o que al menos nos den mas tiempo para prepararnos.

        Durante el examen, note que muchas preguntas eran sobre temas que apenas haviamos visto en clase.
        Intente aser lo mejor posible, pero havian conseptos que no entendia bien. La berdad es que me
        senti muy frustrado porque havia estudiado mucho. Creo que el problema fue que no nos dieron
        suficientes ejemplos practicos antes.

        Cuando termine, able con otros estudiantes y todos tenian la misma opinion. Algunos incluso
        dijeron que ivan a ablar con el director sobre esto. No es justo que nos evaluem sobre cosas
        que no nos an enseñado bien. Ademas, el tiempo que nos dieron no fue sufisiente para terminar
        todas las preguntas. Varios tubimos que dejar ejercicios sin resolver porque no nos alcanso el tiempo.

        Tambien ubo problemas con las instrucciones del examen. Algunas preguntas estavan mal redactadas
        y no se entendia vien que havia que aser. Le pregunte a la profesora pero dijo que no podia
        ayudarnos. Me parese injusto que nos califiquen asi. Espero que al menos tomen en cuenta estos
        problemas cuando revisen los examenes.
        """
    },
    {
        "id": 3,
        "autor": "Autor3",
        "texto": """
        Los resultados del ejercicio de matematicas son incorrectos y no entiendo porque. He revisado
        varias veces todas las operaciones que hice, pero no encuentro donde esta el error. Ya llevo
        tres dias intentando resolver este problema y cada vez me siento mas frustrado. Necesito ayuda
        para encontrar que estoy haciendo mal.

        El profesor nos dijo que era un ejercicio simple, pero para mi no lo es. E intentado diferentes
        metodos para resolverlo pero siempre llego a respuestas diferentes. Lo peor es que ninguna
        coincide con la solucion que nos dieron. Me pregunto si quizas ay algun error en los datos
        del problema o si estoy interpretando mal lo que piden.

        Ayer me quede asta tarde practicando otros ejercicios similares. Pense que si asia mas ejemplos
        podria entender mejor como resolverlo. La verdad es que algunos me salieron vien, pero cuando
        regrese al ejercicio original, volvi a tener los mismos problemas. No se si estoy complicandome
        demasiado o si me falta entender algo fundamental.

        Esta mañana intente buscar ayuda en internet, pero las explicaciones que encontre eran mui
        diferentes a lo que vimos en clase. Creo que voy a tener que pedirle al profesor que me explique
        otra vez. No me gusta molestar tanto, pero ya no se que mas aser. Espero que esta vez pueda
        entender bien como se resuelve este tipo de problemas.

        Lo que mas me preocupa es que el examen es la proxima semana y este tema va a estar incluido.
        Si no logro entenderlo pronto, no se como voy a poder aprovar. E estado pensando en formar un
        grupo de estudio con otros compañeros que tambien tienen dificultades. Quizas entre todos
        podamos ayudarnos a comprender mejor.
        """
    },
    {
        "id": 4,
        "autor": "AngelC",
        "texto": """
        Es un placer recomendar a Pedro Muñoz, quien ha colaborado recientemente con nuestra empresa como desarrollador web junior externo. A pesar de su corta experiencia en el campo, Pedro se ha convertido rápidamente en un activo invaluable para nuestros proyectos.

        Lo que más destaca de Pedro es su extraordinaria capacidad de aprendizaje y adaptación. Su experiencia previa como técnico aeronáutico le ha proporcionado una perspectiva única para resolver problemas, aportando soluciones innovadoras incluso en situaciones complejas.A pesar de ser un colaborador externo, Pedro se ha integrado perfectamente en nuestros procesos. Su actitud positiva, iniciativa y flexibilidad han sido fundamentales para el éxito de nuestros proyectos. Siempre está dispuesto a ir más allá, proponiendo mejoras y adaptándose a las necesidades cambiantes del trabajo.

        Su meticulosidad y precisión, probablemente heredadas de su experiencia en aeronáutica, se reflejan en la alta calidad de su trabajo. Además, su excelente gestión del tiempo y capacidad para cumplir plazos, incluso bajo presión, lo convierten en un colaborador extremadamente confiable.

        En resumen, Pedro ha superado con creces nuestras expectativas, no solo por su rápido aprendizaje técnico, sino por sus excepcionales cualidades personales y profesionales. Recomiendo a Pedro Muñoz sin reservas, convencido de que será un activo excepcional para cualquier equipo.
        """
    }
]