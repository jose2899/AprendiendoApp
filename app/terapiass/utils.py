from datetime import datetime, timedelta

def calculate_start_date(weekday, start_date):
    # Calcular la diferencia entre el día de la semana de la fecha de inicio y el día deseado
    days_until_next_weekday = (weekday - start_date.weekday() + 7) % 7
    # Calcular la fecha del próximo día deseado
    start_date = start_date + timedelta(days=days_until_next_weekday)
    return start_date