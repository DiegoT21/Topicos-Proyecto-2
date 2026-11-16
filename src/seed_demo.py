"""Datos de DEMOSTRACIÓN (ficticios) para probar la interfaz.

Uso (desde la raíz del repo):
    python src/seed_demo.py            # crea tutorias.db con materias, tutores y bloques para los próximos días
    python src/seed_demo.py --reset    # borra las tablas antes

Imprime el código de cada tutor para entrar en tutor.html. Los nombres y correos son inventados.
"""
import sys
from datetime import datetime, time, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import models  # noqa: E402
from app.config import local_now  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402

SUBJECTS = ["Cálculo I", "Física I", "Programación I", "Contabilidad"]
TUTORS = [
    ("Ana Pérez", "ana.perez@utp.ac.pa", ["Cálculo I", "Física I"], [(9, 12), (14, 16)]),
    ("Bruno Díaz", "bruno.diaz@utp.ac.pa", ["Cálculo I"], [(10, 13)]),
    ("Carla Ríos", "carla.rios@utp.ac.pa", ["Programación I"], [(13, 17)]),
    ("Darío Vega", "dario.vega@utp.ac.pa", ["Contabilidad", "Cálculo I"], [(8, 10), (17, 19)]),
]


def main(reset: bool) -> None:
    if reset:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(models.Subject).count():
            print("La base ya tiene datos. Usa --reset para empezar de cero.")
            return
        subjects = {name: models.Subject(name=name) for name in SUBJECTS}
        db.add_all(subjects.values())
        today = local_now().date()
        for name, email, subs, blocks in TUTORS:
            tutor = models.Tutor(name=name, email=email, subjects=[subjects[s] for s in subs])
            db.add(tutor)
            db.flush()
            for offset in range(1, 6):  # desde mañana, 5 días
                day = today + timedelta(days=offset)
                for start, end in blocks:
                    db.add(models.Availability(tutor_id=tutor.id, start_at=datetime.combine(day, time(start)),
                                               end_at=datetime.combine(day, time(end))))
            print(f"Tutor {name:<12} código: {tutor.token}")
        db.commit()
    print("Listo. Datos ficticios de demostración.")


if __name__ == "__main__":
    main("--reset" in sys.argv)
