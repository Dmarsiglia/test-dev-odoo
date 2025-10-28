#!/bin/bash

# Script de gestión de Odoo
# Autor: Asistente IA
# Descripción: Script para iniciar, gestionar y terminar procesos de Odoo

# Colores para el menú
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Directorio del proyecto
PROJECT_DIR="/home/dmarsiglia/dev-odoo/test-dev-odoo"
CONFIG_FILE="$PROJECT_DIR/.env"

# Función para cargar configuración del archivo .env
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${GREEN}Cargando configuración desde $CONFIG_FILE...${NC}"
        source "$CONFIG_FILE"
    else
        echo -e "${RED}Error: No se encontró el archivo de configuración $CONFIG_FILE${NC}"
        echo -e "${YELLOW}Usando valores por defecto...${NC}"
        DB_NAME="milan5"
        MODULES="base"
        ODOO_CONFIG="odoo.conf"
        ODOO_BIN="odoo/odoo-bin"
    fi
}

# Función para mostrar el menú principal
show_menu() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║        GESTOR DE ODOO v1.0           ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Base de datos actual: ${YELLOW}$DB_NAME${NC}"
    echo -e "${BLUE}Módulos a actualizar: ${YELLOW}$MODULES${NC}"
    echo ""
    echo -e "${GREEN}1.${NC} Iniciar Odoo"
    echo -e "${GREEN}2.${NC} Iniciar consola de Odoo"
    echo -e "${GREEN}3.${NC} Terminar procesos de Odoo"
    echo -e "${GREEN}4.${NC} Ver procesos de Odoo activos"
    echo -e "${GREEN}5.${NC} Editar configuración"
    echo -e "${GREEN}6.${NC} Crear base de datos"
    echo -e "${RED}7.${NC} Salir"
    echo ""
    echo -ne "${PURPLE}Selecciona una opción [1-7]: ${NC}"
}

# Función para iniciar Odoo
start_odoo() {
    echo -e "${GREEN}Iniciando Odoo...${NC}"
    echo -e "${YELLOW}Base de datos: $DB_NAME${NC}"
    echo -e "${YELLOW}Módulos a actualizar: $MODULES${NC}"
    echo ""
    
    cd "$PROJECT_DIR" || exit 1
    
    # Comando para iniciar Odoo
    COMMAND="python3 $ODOO_BIN --dev=xml -c $ODOO_CONFIG -d $DB_NAME -u $MODULES"
    
    echo -e "${BLUE}Ejecutando: $COMMAND${NC}"
    echo ""
    
    # Ejecutar el comando
    eval $COMMAND
}

# Función para iniciar la consola de Odoo
start_console() {
    echo -e "${GREEN}Iniciando consola de Odoo...${NC}"
    echo -e "${YELLOW}Base de datos: $DB_NAME${NC}"
    echo ""
    
    cd "$PROJECT_DIR" || exit 1
    
    # Comando para iniciar la consola de Odoo
    COMMAND="python3 $ODOO_BIN shell -c $ODOO_CONFIG -d $DB_NAME"
    
    echo -e "${BLUE}Ejecutando: $COMMAND${NC}"
    echo ""
    
    # Ejecutar el comando
    eval $COMMAND
}

# Función para terminar procesos de Odoo
kill_odoo_processes() {
    echo -e "${RED}Buscando procesos de Odoo...${NC}"
    
    # Buscar procesos de Odoo
    ODOO_PIDS=$(pgrep -f "odoo-bin")
    
    if [ -z "$ODOO_PIDS" ]; then
        echo -e "${YELLOW}No se encontraron procesos de Odoo ejecutándose.${NC}"
    else
        echo -e "${YELLOW}Procesos de Odoo encontrados:${NC}"
        ps aux | grep odoo-bin | grep -v grep
        echo ""
        
        echo -ne "${RED}¿Estás seguro de que quieres terminar estos procesos? [y/N]: ${NC}"
        read -r confirm
        
        if [[ $confirm =~ ^[Yy]$ ]]; then
            # CORRECCIÓN DE LA LÍNEA 110
            echo "$ODOO_PIDS" | xargs kill -9
            sleep 1
            echo -e "${GREEN}Procesos de Odoo terminados.${NC}"
        else
            echo -e "${YELLOW}Operación cancelada.${NC}"
        fi
    fi
    
    echo ""
    echo -ne "${BLUE}Presiona Enter para continuar...${NC}"
    read -r
}

# Función para ver procesos activos
show_processes() {
    echo -e "${BLUE}Procesos de Odoo activos:${NC}"
    echo ""
    
    ODOO_PROCESSES=$(ps aux | grep odoo-bin | grep -v grep)
    
    if [ -z "$ODOO_PROCESSES" ]; then
        echo -e "${YELLOW}No hay procesos de Odoo ejecutándose.${NC}"
    else
        echo "$ODOO_PROCESSES"
    fi
    
    echo ""
    echo -ne "${BLUE}Presiona Enter para continuar...${NC}"
    read -r
}

# Función para editar configuración
edit_config() {
    echo -e "${BLUE}Configuración actual:${NC}"
    echo -e "${YELLOW}Base de datos: $DB_NAME${NC}"
    echo -e "${YELLOW}Módulos: $MODULES${NC}"
    echo ""
    
    echo -ne "${GREEN}¿Quieres editar la configuración? [y/N]: ${NC}"
    read -r edit_confirm
    
    if [[ $edit_confirm =~ ^[Yy]$ ]]; then
        echo -ne "${BLUE}Nueva base de datos (actual: $DB_NAME): ${NC}"
        read -r new_db
        if [ ! -z "$new_db" ]; then
            DB_NAME="$new_db"
        fi
        
        echo -ne "${BLUE}Nuevos módulos separados por comas (actual: $MODULES): ${NC}"
        read -r new_modules
        if [ ! -z "$new_modules" ]; then
            MODULES="$new_modules"
        fi
        
        # Actualizar el archivo de configuración
        cat > "$CONFIG_FILE" << EOF
# Configuración de la base de datos
DB_NAME=$DB_NAME

# Módulos a actualizar (separados por comas)
MODULES=$MODULES

# Configuración adicional
ODOO_CONFIG=odoo.conf
ODOO_BIN=odoo/odoo-bin
EOF
        
        echo -e "${GREEN}Configuración actualizada correctamente.${NC}"
    fi
    
    echo ""
    echo -ne "${BLUE}Presiona Enter para continuar...${NC}"
    read -r
}

# Función para crear base de datos
create_database() {
    echo -e "${GREEN}Creando base de datos...${NC}"
    echo -e "${YELLOW}Base de datos: $DB_NAME${NC}"
    echo -e "${YELLOW}Módulos a instalar: $MODULES${NC}"
    echo ""

    cd "$PROJECT_DIR" || exit 1

    # Comando para crear base de datos con los módulos especificados
    COMMAND="python3 $ODOO_BIN -c $ODOO_CONFIG -d $DB_NAME --init=$MODULES"

    echo -e "${BLUE}Ejecutando: $COMMAND${NC}"
    echo ""

    # Ejecutar el comando
    eval $COMMAND

    echo -e "${GREEN}Base de datos creada correctamente.${NC}"
}

# Función principal
main() {
    # Cargar configuración
    load_config
    
    while true; do
        show_menu
        read -r option
        
        case $option in
            1)
                start_odoo
                echo ""
                echo -ne "${BLUE}Presiona Enter para continuar...${NC}"
                read -r
                ;;
            2)
                start_console
                echo ""
                echo -ne "${BLUE}Presiona Enter para continuar...${NC}"
                read -r
                ;;
            3)
                kill_odoo_processes
                ;;
            4)
                show_processes
                ;;
            5)
                edit_config
                ;;
            6)
                create_database
                ;;
            7)
                echo -e "${GREEN}¡Hasta luego!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Opción no válida. Por favor selecciona una opción del 1 al 7.${NC}"
                sleep 2
                ;;
        esac
    done
}

# Verificar que estamos en el directorio correcto
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Error: No se encontró el directorio del proyecto $PROJECT_DIR${NC}"
    exit 1
fi

# Ejecutar función principal
main