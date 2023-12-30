import evdev


class IdentifierReader:
    raspberry = ""  # v3 or v4

    """
    #Diagrama raspberry ubicaciones fisicas (RaspBerry v4)
    [1.3/input0] [1.1/input0]
    [1.4/input0] [1.2/input0] [Entrada Ethernet]

    #(OLD) Diagrama raspberry ubicaciones fisicas (RaspBerry v3)

                        [usb-1.2/input0] [usb-1.4/input0]
    [Entrada Ethernet]  [usb-1.3/input0] [usb-1.5/input0]

    """

    all_readers_conected = True  # Esta variable indica que TODOS los lectores estan conectados, independientemente de cuantos sean
    one_device_disconnected = False  # Esta variable indica que UNO de los dispositivos esta desonectado

    ubicacion_fisica_lector = ""  # Cuando es un solo lector (Ya sea que registre entradas y salidas, solamente entradas, etc)
    ubicacion_fisica_lector_entrada = ""  # Cuando hay un lector dedicado a entradas
    ubicacion_fisica_lector_salida = ""  # Cuando hay un lector dedicado a salidas

    def start_setup(self, raspberry_version="v4"):
        self.set_raspberry_version(raspberry_version)
        self.initialize_ports_names()

    def set_raspberry_version(self, version):
        self.raspberry = version

    def initialize_ports_names(self):
        if self.raspberry == "v4":
            ub_fisc_string = "usb-0000:01:00.0-"

            self.ubicacion_fisica_lector = ub_fisc_string + "1.2/input0"
            self.ubicacion_fisica_lector_entrada = ub_fisc_string + "1.4/input0"
            self.ubicacion_fisica_lector_salida = ub_fisc_string + "1.2/input0"

        elif self.raspberry == "v3":
            ub_fisc_string = "usb-3f980000."

            self.ubicacion_fisica_lector = ub_fisc_string + "usb-1.3/input0"
            self.ubicacion_fisica_lector_entrada = ub_fisc_string + "usb-1.3/input0"
            self.ubicacion_fisica_lector_salida = ub_fisc_string + "usb-1.5/input0"

    def list_connected_devices():
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        print("====================== (START) List Devices ======================")
        for device in devices:
            print("Name:", device.name)
            print("Physical Location:", device.phys)
            print()
        print("====================== (END) List Devices ======================\n")

    def leer_identificador(self, puerto_lector, tipo_registro):
        lector = evdev.InputDevice(puerto_lector)

        codigo_rfid = []
        try:
            for event in lector.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    codigo = evdev.categorize(event)
                    if codigo.keystate == 1:  # Solo considerar eventos de pulsación de tecla, no de liberación
                        if codigo.keycode == 'KEY_ENTER':
                            break
                        elif codigo.keycode.startswith('KEY_'):
                            digito = codigo.keycode.split('_')[1]  # Obtener el dígito eliminando 'KEY_' del código
                            codigo_rfid.append(digito)
            return ''.join(codigo_rfid)
        except FileNotFoundError:
            self.all_readers_conected = False
            print(f"[ERROR] El lector de [{tipo_registro}] no está conectado")
            return None
        except OSError as e:
            self.all_readers_conected = False
            if e.errno == 19:
                print(f"[ERROR] El lector de [{tipo_registro}] se desconectó")
            else:
                raise
            return None
        except Exception as e:
            self.all_readers_conected = False
            print("[ERROR] Ocurrió una excepción inesperada lectores:", str(e))
            return None