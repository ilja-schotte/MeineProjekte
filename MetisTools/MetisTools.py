

import sqlalchemy
import traceback
import pandas as pd




class DBConnector():

    """
    AUTOR:          Ilja Schotte 
    AKTUALISIERT:   18.06.2026

    BESCHREIBUNG:
        Stellt eine Datenbankverbindung zur Mirakel-Datenbank her.
        
    ARGS:
        db_name		        [str]	Name der Datenbank zu der eine Verbindung 
                                        hergestellt werden soll (notwendig).

        db_hostname 	    [str]	Hostname der Datenbank (notwendig).
        db_hostname_alt     [str]	Alternativer Hostname der Datenbank (notwendig).
        db_service	        [str]	Servicename der Datenbank (notwendig).
        db_port		        [str]	Port zur Verbindung mit derDatenbank (notwendig).
        db_user		        [str]	Benutzername (notwendig).
        db_pwd		        [str]	Passwort (notwendig).
        db_conn_string_raw  [str]   Verbindungsstring zur Datenbank ohne notwendige 
                                    Argumente. (notwendig)
                                    
        arraysize	        [int]	Maximale Anzahl der Abfrageergebnisse (notwendig).
        
    RETURN:
        engine              [object]    Eine Datenbankverbindung (Pointer).  
    """


    def __init__(self,
            db_name: str, 				 
            db_hostname: str, 			
            db_hostname_alt: str, 			
            db_service: str,			
            db_port: str,				
            db_user: str,				
            db_pwd: str,
            db_conn_string_raw: str,
            db_arraysize: int=1000,
        ):	
        
        self._db_name = str(db_name)
        self._db_hostname = str(db_hostname)		
        self._db_hostname_alt = str(db_hostname_alt)	
        self._db_service = str(db_service)
        self._db_port = str(db_port)			
        self._db_user = str(db_user)			
        self._db_pwd = str(db_pwd)
        self._db_conn_string_raw = str(db_conn_string_raw)
        self._db_arraysize = db_arraysize
        
    # ========================================================================================================
    
    def show_parameter(self):
    
        """
            Zeigt die Argumente zur Datenbankverbindung.
        """
        try:
            print(f"""
            db_name:          {self._db_name}
            db_hostname:      {self._db_hostname}
            db_hostname_alt:  {self._db_hostname_alt}
            db_service:       {self._db_service}
            db_port:          {self._db_port}
            db_user:          {self._db_user}
            db_pwd:           {self._db_pwd}
            arraysize:        {self._db_arraysize}
            """)
            
            
        except Exception as e:
            print(f'FEHLER: Anzeige der Datenbank-Parameter.')
            print(f'-> {e}')
            print(traceback.format_exc())

    # ========================================================================================================

    def __enter__(self):

        # Direkt verbinden.
        self.connect()

        return self

    # ========================================================================================================

    def __exit__(self, exc_type, exc_value, traceback):

        # Prüfen, ob die Engine überhaupt existiert, bevor man sie schließt
        if hasattr(self, '_db_engine'):
            self._db_engine.dispose()
            print(f'Verbindung zur Datenbank geschlossen.')

        return False
    
    # ========================================================================================================
        
    def connect(self):
    
        """
        BESCHREIBUNG:
            Erstellt die Verbindung zur Mirakel-Datenbank.
            Erstellt aus dem Rohstring zur Datenbankverbindung einen validen String
            und übergibt diesen zur Herstellung einer Datenbankverbindung.
        """
    
        try:
            # Erstellt den DNS-String
            self._db_conn_string = self._db_conn_string_raw.format(
                db_hostname=self._db_hostname,
                db_port=self._db_port,
                db_hostname_alt=self._db_hostname_alt,
                db_service=self._db_service
            )

            self._db_engine = sqlalchemy.create_engine(
                "oracle+oracledb://@", 
                connect_args={
                    "user": self._db_user, 
                    "password": self._db_pwd, 
                    "dsn": self._db_conn_string
                }
            ).execution_options(
                yield_per=self._db_arraysize 
            )
                                            
            if hasattr(self, '_db_engine'): 
                print(f'Erfolgreich mit Datenbank verbunden.')

        except Exception as e:
            print(f'FEHLER: Beim Erstellen der Datenbankverbindung:')
            print(f'-> {e}')
            print(traceback.format_exc())

    # ========================================================================================================
            
    def request(self, sql:str) -> pd.DataFrame:
    
        """
        BESCHREIBUNG:
            Nimmt ein SQL-Statement entgegen und führt es entsprechend aus.
            Liefert als Rückgabeobjekt einen Pandas DataFrame.
            
        ARGS:
            sql             [str]		    ...	SQL-statement
        
        RETURN:
            df_result	 	[pd.DataFrame]	...	Ein DataFrame (pandas) mit dem Abfrageergebnissen. 
        """
        
        if not isinstance(sql, str):
            raise TypeError(f'Das SQL-Statement muss von Typ "string" sein nicht {type(sql)}')

        try:
            return pd.read_sql(sql=sqlalchemy.text(sql), con=self._db_engine)
        
        except Exception as e:
            print(f'FEHLER: Beim Datenbankabruf:')
            print(f'-> {e}')
            print(traceback.format_exc())



# ======================================================================================
# ======================================================================================
# ======================================================================================



class Mapper():

    """
    AUTOR:          Ilja Schotte 
    AKTUALISIERT:   22.06.2026

    BESCHREIBUNG:
        Erstellt aus Punktdaten eine 2d-Karte eines bestimmten Areals.
        Das Areal kann entweder als Ländername oder als ein Quadrat mit Hilfe von
        Koordinaten definiert werden.
        
    ARGS:
        data		[pd.DataFrame]	Die Daten müssen als pandas.DataFrame vorliegen.
        col_values  [str]           Spaltenname des unter data übergebenen
                                    pandas.DataFrames der die Werte beinhaltet.
                                    (notwendig)
                                    
        col_lat     [str]           Spaltenname des unter data übergebenen
                                    pandas.DataFrames der die Werte der geografischen
                                    Breite der Messfunkte beinhaltet.
                                    (notwendig)

        col_lon     [str]           Spaltenname des unter data übergebenen
                                    pandas.DataFrames der die Werte der geografischen
                                    Länge der Messfunkte beinhaltet.
                                    (notwendig)
        
        area        [str]           Nur Ländername oder "square". 
                                    Gültige Ländernamen: 'germany'.
                                    Defaultwert: 'germany'
                                    (optional)

        coords      [dict]          Ist area="square", dann muss unter coords ein
                                    dictionary folgender Form geliefert werden:
                                    {'NW': (lat[float], lon[float]),
                                     'NE': (lat[float], lon[float]),
                                     'SW': (lat[float], lon[float]),
                                     'SE': (lat[float], lon[float])}

                                    Die 4 Schlüssel liefern die geografischen Eckpunkte
                                    'NW': northwest
                                    'NE': northeast
                                    'SW': southwest
                                    'SE': southeast
                                    des definierten Quadrats.

        interpol    [str]           Wird interpol ein String übergeben, so definiert er
                                    die Art der durchzuführenden Interpolation der unter
                                    data übergebenen Punktwerte. Das Resultat ist eine
                                    in die Fläche interpolierte Repräsentation der
                                    Datenpunkte.       

    RETURN:
         
    """

    # Tuple der aktuell unterstützten Länder
    supported_areas = ('germany', 'square')   

    def __init__(self, 
            data: pd.DataFrame,
            col_values: str,
            col_lat: str,
            col_lon: str,
            area: str,
            coords: dict[
                str, tuple[float, float], 
                str, tuple[float, float], 
                str, tuple[float, float], 
                str, tuple[float, float]]
                ={},
            interpol: str=''):
        

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                (
                    f'Datensatz: "data" muss vom Typ <pandas.DataFrame> sein, '
                    f'aktuell: {type(data)}')
                )
        
        if data.empty:
            raise Exception(f'Datensatz: "data" ist leer!')
        
        if area not in self.supported_areas:
            raise ValueError(
                (
                    f'Gewählte Region: "area"={area} wird nicht unterstützt. '
                    f'Aktuell unterstützte Regionen sind: {self.supported_areas}'
                )
            )

        if area == 'square':
            if not isinstance(coords, dict):
                raise TypeError(
                    (
                        f'Die übergebenen Koordinaten "coords" müssen vom Typ <dict> sein, '
                        f'aktuell: {type(coords)}'
                    )
                )
            
            if not coords:
                raise ValueError(
                    (
                        f'Achtung! "area"="square" erfordert die Angabe eines Dictionary'
                        f' "coords". Das Dictionary "coords" ist leer.'
                    )
                )

        self._data = data
        self._col_values = col_values
        self._col_lat = col_lat
        self._col_lon = col_lon
        self._area = area
        self._coords = coords


    def show_parameters(self):

        """
            Zeigt die Argumente des Objekts.
        """
        try:
            print(f"""
            Datensatz:
                Anzahl Messwerte:       {len(self._data.index)}
                Spaltenname (values):   {self._col_values}
                Spaltenname (lat.):     {self._col_lat}
                Spaltenname (lon.):     {self._col_lon}
            Region:                     {self._area}
            Koordinaten:                {self._coords}
            """)
            
            
        except Exception as e:
            print(f'FEHLER: Anzeige der Parameter.')
            print(f'-> {e}')
            print(traceback.format_exc())
