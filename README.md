# DinoAI
DinoAI es un juego hecho en python en conjunto con pygame diseñado para poder probar algoritmos, redes neuronales o Inteligencias Artificial para determinar su rendimiento en un juego.
El juego es muy similar al dinosaurio de Chorme. Existe un dinosaurio tratando de saltar obstaculos, en este caso, flores.

------------

Para este juego se ha implementado 2 algoritmos y 2 modos de juegos, descritos a continuación.

## Modos de juego
### Normal
El modo normal no depende de ningun algoritmo, es el modo en el que el usuario es el que desempeña el juego, una vez pierda la ventana del juego es cerrada.

### Algoritmo
El modo Algoritmo es en el cual se elije algun algoritmo para poder tomar el control y jugar, para este caso no es necesario especificar el modo de juego en el programa, si no es normal será utilizado algun algoritmo.

------------

## Algoritmos
Para esta versión del juego se ha implementado 2 algoritmos: genético y de clasificación binaria. Los datos utilizados para que cualquiera de los dos algoritmos tomen la decisión y ejecuten la acción correcta son: la distacia del objeto y la velocidad (esto solo para la clasificación binaria)

### Genético
El algoritmo genético empieza generando un "padre" aleatório y de ahí parte su descendencia, para evaluar al individuo se lo compara con sus "padres" o generaciones anteriores. La comparación se hace restando su fitnes (desempeño del nuevo gen) con su anteroir gen (o padre), mientras el resultado sea mayor signifca que hay un "avance"

En caso no se vea un avance existe la posibilidad de que el algorito elija retroceder algunas generaciones o escoger a un gen que haya tenido un buen desempeño. Cada 200 generaciones se hace una verificación general.

Si el actual individuo demuestra ser superior se lo elige y se genera otro, en caso el nuevo tenga un desempeño menor se optará por el anteroir, ha esto se le denomina "retroceder".

Para generar al nuevo individuo se toma en cuenta a sus dos generaciones anterioires y se hace un calculo matemático dependiendo de los resultados.
En la mayoría de veces se nota que la distancia mínima para hacer el salto se va reduciendo, si llega muy bajo aumentará drásticamente y luego volvera a disminuir progresivamente.

### Clasificación binaria
Para el algoritmo de clasificación binaria se utilizo el módulo `sklearn` y se usó la clase `tree` para hacer la elaboración de un arbol. Los datos fueron recolectodos durante una partida de un jugador y etiquetados manualmente, solo se optó por tener 10 datos. El algoritmo evalua la entrada distancia (`dist`) y velocidad (`speed`) y retorna `0` en caso de no saltar y `1` en caso de optar por el salto.

Ambos algoritmos estan disponibles en este mismo repositorio con los nombres de `decision_bin.py` para el algoritmo de clasificación binaria y `decision_gen.py` para el algoritmo genético.

------------

## Uso
En este caso aún no se implementa una CLI ni un archivo `.exe` por lo que para probarlo se tiene que clonar el repositorio y desde la terminal ejecutar el comando `python game.py`. Por defecto usa el algoritmo de clasificación, en caso quieras cambiar el algoritmo, lo puedes hacer de esta forma

En el archivo `game.py` en la ultima línea de código se hace el llamado a la función `runner()` a la cual se le pasa el algoritmo a utilizar:
- Para el algoritmo de clasificación la palabra es `clasifier`
```python
runner(alg="clasifier")
```
- Para el algoritmo genético se utiliza `genetic`
```python
runner(alg="genetic")
```
En caso se quiera el modo normal, solo se especifica el parámetro `mode`, no es necesario especificar un parámetro `alg` pues no es necesario y en caso de ser pasado será ignorado.
```python
runner(mode="normal")
```
------------

## Colaborar
Este proyecto aún tine muchas cosas por mejorar, asi que te invito a que colabores en este proyecto, clona el repositorio y realiza los cambios necesario luego simplemente envia un petición y con gusto la revisaré ^_^