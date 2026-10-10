# OX212 · Public seal registry

A public, independent copy of every OX212 seal.

**What a seal is.** Every hour, OX212 gathers the fingerprint of everything it recorded in that hour: Guard
receipts, sessions read by the engine, forecasts and their checks, interventions and what happened next. Those
fingerprints form a Merkle tree; its root is chained to the previous seal and written into a small public manifest
(`ox212-seal-<id>.json`). The manifest's sha256 is anchored in Bitcoin with [OpenTimestamps](https://opentimestamps.org),
an open standard.

**What is not here.** No personal data: only fingerprints, counts and times. Every record carries a private salt, so
nothing can be learned from a fingerprint. If someone deletes their account, OX212 deletes that salt too.

**Why this repository.** Git's history is an independent witness of when each seal was published. Manifests are never
rewritten here: if a seal ever changed, it would show.

## How to verify a seal

1. Install the official client: `pip install opentimestamps-client`.
2. In the seal's folder, run `ots verify ox212-seal-<id>.json.ots`.
   The second proof, from another calendar: `ots verify -f ox212-seal-<id>.json ox212-seal-<id>.json.b.ots`.
3. To walk the chain, `scripts/check_chain.py` checks that every seal continues the one before:
   `chain = sha256(prev_chain || root)`.

For the first hours a proof says «pending». Once the calendar includes the fingerprint in a Bitcoin block, the proof
updates here on its own and points to that block.

## Rules

- `leaf = sha256(salt || sha256(content))`: each record, with its private salt.
- `node = sha256(0x01 || left || right)`: the tree's nodes; an odd node is paired with itself.
- `chain = sha256(prev_chain || root)`: each seal continues the one before.
- What is anchored in Bitcoin is the `sha256` of the seal's manifest, exactly as published.

A trader can verify their own records with their evidence package: content, salt and path to the root.

---

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
