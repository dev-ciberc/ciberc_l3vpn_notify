# Crear el paquete
python3 setup.py bdist_wheel

# Instalar el paquete
python3 -m pip install dist/ciberc_l3vpn_notify-0.1-py3-none-any.whl --force-reinstall
