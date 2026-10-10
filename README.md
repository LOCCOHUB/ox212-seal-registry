# OX212 · Registro público del sello

Este repositorio guarda una copia pública e independiente de cada sello de OX212.

**Qué es un sello.** Cada hora, OX212 junta la huella de todo lo que ha registrado en esa hora: recibos del Guard,
días leídos por el motor, previsiones y su comprobación, intervenciones y lo que pasó después. Con esas huellas forma
un árbol, encadena su raíz con la del sello anterior y escribe un pequeño documento público (`ox212-seal-<id>.json`).
La huella de ese documento se ancla en Bitcoin con [OpenTimestamps](https://opentimestamps.org), un estándar abierto.

**Qué no hay aquí.** Ningún dato personal: solo huellas, recuentos y horas. Cada registro lleva una sal privada, así
que nadie puede deducir nada a partir de una huella. Si alguien borra su cuenta, OX212 borra también esa sal.

**Por qué este repositorio.** El historial de git es un testigo independiente de cuándo se publicó cada sello. Los
documentos de los sellos nunca se reescriben aquí: si un sello cambiase, se vería.

## Cómo comprobar un sello

1. Instala el cliente oficial: `pip install opentimestamps-client`.
2. En la carpeta del sello, ejecuta: `ots verify ox212-seal-<id>.json.ots`.
   La segunda prueba, de otro calendario: `ots verify -f ox212-seal-<id>.json ox212-seal-<id>.json.b.ots`.
3. Para recorrer la cadena, `scripts/check_chain.py` comprueba que cada sello continúa al anterior:
   `chain = sha256(prev_chain || root)`.

Las primeras horas la prueba dice «pending». Cuando el calendario incluye la huella en un bloque de Bitcoin, la
prueba se actualiza aquí sola y ya apunta a ese bloque.

## Reglas

- `leaf = sha256(salt || sha256(content))`: cada registro, con su sal privada.
- `node = sha256(0x01 || left || right)`: los nodos del árbol; un nodo impar se empareja consigo mismo.
- `chain = sha256(prev_chain || root)`: cada sello continúa al anterior.
- Lo que se ancla en Bitcoin es el `sha256` del documento del sello, tal cual está publicado.

Un trader puede comprobar sus propios registros con su paquete de evidencia: contenido, sal y camino hasta la raíz.

---

# OX212 · Public seal registry

A public, independent copy of every OX212 seal. Every hour, the fingerprints of everything OX212 recorded (Guard
receipts, engine readings, forecasts and their checks, interventions and their outcomes) form a Merkle tree; its
root is chained to the previous seal and written into a small public manifest whose sha256 is anchored in Bitcoin
with OpenTimestamps. No personal data: only salted hashes, counts and times. Verify with
`ots verify ox212-seal-<id>.json.ots`, and the chain with `scripts/check_chain.py`.
