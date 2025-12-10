# Naming of Chemical Substances

---


---

## 101. Foreword

This is not a comprehensive nomenclature manual for all of chemistry but a specific guide to how chemical names in the NIST spectral library are constructed, ordered, and formatted. The primary goal is to enable a user to rapidly identify specific chemical substances. Except for common chemical names, the nomenclature generally follows the rules of the International Union of Pure and Applied Chemistry (IUPAC) but is adapted for the use in the NIST libraries, including quickly comprehending the chemicals in a list. Every **unique chemical structure** should receive one **unique name**.

To name a chemical, follow these steps:

1. Determine if a common name exists that is widely used in scientific literature. Do not use popular common names that are not typically used in the scientific literature, such as alcohol for ethyl alchohol, or that refer to mixtures, like vinegar.
2. If YES: Use the common name, applying formatting rules (inversion, punctuation, etc.) as needed
3. If NO: Construct a systematic structure-based name following all rules below. The names should be **structure-based**, aiming for **consistency, uniqueness, and retrievability** in databases.

For ease of comparison, the section numbers follow the [Naming and Indexing of
Chemical Substances for
Chemical Abstracts](https://web.cas.org/marketing/pdf/indexguideapp.pdf).

## 104. Inversion of Names

To group related substances, index names are inverted. The **Heading Parent** (the main part of the molecule) is listed first, followed by a comma, and then the **Substituents**. If a derivative (like an ester or salt) is present, it appears in the **Modification** at the end of the name.

- *Example:* **Acetic acid, 2-(2,4-dichlorophenoxy)-, methyl ester**
  - *Heading Parent:* Acetic acid
  - *Substituent:* 2-(2,4-dichlorophenoxy)-
  - *Modification:* methyl ester

## 106. Order of Precedence of Compound Classes

When a compound contains multiple functional groups, the Heading Parent is chosen based on a strict order of precedence. The class higher in the list becomes the parent, while lower classes are expressed as prefixes (substituents).

1. **Acids**: Carboxylic acids rank highest among common organic functions.
    - *Example:* **Benzoic acid, 4-amino-** (Acid is parent; amine is substituent).
2. **Amides**: Lower than acids but higher than nitriles.
    - *Example:* **Benzamide, 3-methyl-**.
3. **Nitriles**:
    - *Example:* **Benzonitrile, 2-fluoro-**.
4. **Aldehydes**:
    - *Example:* **Benzaldehyde, 4-methoxy-**.
5. **Ketones**:
    - *Example:* **2-Butanone, 3-chloro-**.
6. **Alcohols**:
    - *Example:* **1-Butanol, 2-methyl-**.
7. **Amines**:
    - *Example:* **1-Butanamine, N-butyl-**.

## 108. Punctuation

Punctuation is critical for clarity.

- **Commas** separate locants (e.g., *2,3-dichloro*) and the parent from substituents in inverted names.
- **Hyphens** join locants to names (e.g., *4-chloro-*).
- **Italics** are used for locants like *N-* or *O-* and stereochemical descriptors like *cis-* or *trans-*.
  - *Example:* **Acetamide, N-phenyl-**.
- **Greek Letters:** The dataset employs a specific ASCII-compatible format for special characters and punctuation to ensure machine readability. Greek characters are not used as symbols (e.g., $\alpha, \beta$). Instead, they are written phonetically, enclosed by periods.
  - **.alpha.** is used for alpha.
  - **.beta.** is used for beta.
  - **.eta.** is used for eta (hapticity).
  - **.mu.** is used for mu (bridging).
  - **.pi.** is used for pi (bonding).
  - *Examples:* **.beta.-Alanine**; **.pi.-Cyclopentadienyl...**; **1,1,1,2,3,3,3-Heptafluoro-2-methoxypropane** (Note the commas separating locants).

## 109. Enclosing Marks

Parentheses `()` and brackets `[]` are used to prevent ambiguity, particularly when a substituent itself is substituted (compound radicals).

- *Example:* **Benzoic acid, 4-\[\[(2,4-dichlorophenyl)amino\]carbonyl\]-**
  - Here, brackets enclose the complex substituent group attached to the parent Benzoic acid.

## 110. Multiplicative Prefixes

Prefixes such as *di-*, *tri-*, *tetra-* are used for simple substituents. For compound substituents or to avoid ambiguity, *bis-*, *tris-*, *tetrakis-* are used.

- *Example (Simple):* **Benzene, 1,3-dichloro-**.
- *Example (Complex):* **Ethanone, 1,1'-(1,3-phenylene)bis-**.

## 113. Order of Citation in Modifications

Derivatives in the modification phrase (following the inverted name) are cited in a specific order: salts, then esters, then other functional derivatives.

- *Example:* **Glycine, N-acetyl-, methyl ester** (Ester cited in modification).

## 114-118. Locants

Locants (numbers or letters) indicate the position of substituents on the skeleton.

- **Low Numbering:** The skeleton is numbered to give the lowest possible locants to the principal group, then to double bonds, then to substituents.
  - *Example:* **2-Butanone** (Not 3-Butanone).
- **Heteroatoms:** In acyclic chains with heteroatoms, locants are assigned to the heteroatoms where possible.
- **Multiplicative Nomenclature:** When two identical parents are linked, locants distinguish the positions.
  - *Example:* **1,1'-Biphenyl, 4,4'-dichloro-**.

## 122. Tautomers

For compounds that exist in equilibrium between two forms (tautomers), a single preferred form is chosen for the index name to avoid scattering. Common examples include ketones vs. enols and amides vs. imidic acids.

- *Example:* **2-Pyridinone** is preferred over *2-Pyridinol* when the oxo-form is dominant or preferred by rule.
- *Example:* **2,4(1H,3H)-Pyrimidinedione** is used instead of the Uracil trivial name.

## 130. Substitutive Nomenclature

This is the fundamental system used for most organic compounds in the list. A hydrogen atom on the parent skeleton is "substituted" by a radical (group).

- *Examples:* **Benzene, chloromethyl-** (A hydrogen on benzene is replaced by a chloromethyl group).

## 135. Indicated Hydrogen

For ring systems where maximum unsaturation is possible but one position remains saturated, the "Indicated Hydrogen" convention is strictly observed.

- **Rule:** The position of the saturated atom is indicated by a locant and a capital 'H' immediately preceding the ring name.
- **Priority:** This indicator appears at the very beginning of the name.
- *Examples from Data:*
  - **1H-1,2,4-Triazol-5-amine** (The nitrogen at position 1 has the hydrogen).
  - **2H-1,3-benzodioxole** (The carbon at position 2 is saturated).
  - **5H-Cyclohepta-1,4-dioxin**.

---

## Molecular Skeletons (¶140–163A)

### 141. Acyclic Hydrocarbons

Saturated chains are named Alkanes (e.g., *Butane*, *Pentane*). Unsaturated chains take suffixes like *-ene* (Alkenes) or *-yne* (Alkynes).

- *Examples:* **1-Pentene**; **1-Octyne**.

### 145. Cycloalkanes and Cycloalkenes

Monocyclic hydrocarbons are named by attaching the prefix *cyclo-* to the acyclic name.

- *Examples:* **Cyclopentane**; **Cyclohexene**.

### 146. Monocyclic Heterocycles

Rings containing heteroatoms (N, O, S) are named using Hantzsch-Widman stems or retained trivial names.

- *Examples:* **Pyridine** (6-membered, N); **Furan** (5-membered, O); **Thiophene** (5-membered, S); **Piperidine** (saturated Pyridine).

### 147. Fused Ring Systems

Polycyclic systems formed by sharing adjacent atoms are named by combining component names or using trivial names.

- *Examples:* **Naphthalene**; **Quinoline** (Benzene fused to Pyridine); **Benzofuran**.

### 148. Bridged Ring Systems

Systems with shared atoms that are not adjacent are named using the Von Baeyer system (e.g., Bicyclo\[x.y.z\]alkane).

- *Examples:* **Bicyclo\[2.2.1\]heptane**; **Adamantane**.

### 156. Spiro Systems

Systems where two rings share a single atom are named *Spiro*.

- *Example:* **Spiro\[4.5\]decane**.

### 159. Boron Compounds

Neutral boron hydrides are named *Borane*.

- *Example:* **Borane, trifluoro-**. Complex organoboron compounds are named as derivatives.
- *Example:* **9-Borabicyclo\[3.3.1\]nonane**.

---

## Principal Chemical Groups (Suffixes) (¶164–177)

### 165. Carboxylic Acids

Named with the suffix *-oic acid* (acyclic) or *-carboxylic acid* (cyclic attached carbon).

- *Examples:* **Heptanoic acid**; **Cyclopropanecarboxylic acid**.

### 166. Acid Halides

Named by changing *-ic acid* to *-yl halide*.

- *Examples:* **Acetyl chloride**; **Benzoyl chloride**.

### 167. Amides

Named by changing *-oic acid* to *-amide*.

- *Examples:* **Benzamide**; **Butanamide**.

### 168. Nitriles

Named by adding *-nitrile* to the alkane name or changing *-ic acid* to *-onitrile*.

- *Examples:* **Acetonitrile**; **Benzonitrile**.

### 170. Ketones

Named using the suffix *-one*.

- *Examples:* **2-Propanone** (Acetone); **Cyclohexanone**.

### 171. Alcohols

Named using the suffix *-ol*.

- *Examples:* **Ethanol**; **Cyclohexanol**.

### 173. Thiols

Named using the suffix *-thiol*.

- *Example:* **1-Butanethiol**.

### 174. Amines

Named using the suffix *-amine*.

- *Examples:* **Benzenamine** (Aniline); **1-Butanamine**.

---

## Compound Classes (¶178–201)

### 180. Anions

Anions are generally named by changing the parent ending.

- *Example:* **Acetate** (from Acetic acid, found in salt names).

### 185. Esters

There are two distinct naming styles for esters, corresponding to indexing complex acids versus common nomenclature for simpler ones.

#### Style A: Inverted (Acid Header)**

- **Rule:** The parent acid is the heading. The alcohol portion is listed as a modification following a comma, ending with the word "ester".
- *Examples:*
  - **Propanoic acid, 2-chloro-, ethyl ester**.
  - **3-Isoxazolecarboxylic acid, 4-(chloromethyl)-5-methyl-, methyl ester**.
  - **Acetic acid, bromo-, ethyl ester**.

#### Style B: Non-Inverted (Alkyl Alkanoate)**

- **Rule:** The alkyl group (alcohol derived) is named first, followed by the acid derivative (alkanoate).
- *Examples:*
  - **Methyl 2,4,6-trichloro-3,5-dimethoxybenzoate**.
  - **Ethyl 2-nitropropionate**.

### 189. Hydrazides

Derivatives of hydrazine with acid groups.

- *Example:* **Acetic acid, hydrazide**.

### 190. Hydrazones and Oximes

Oximes are treated as functional derivatives of their parent aldehydes or ketones.

- **Rule:** The name is constructed as [Parent Aldehyde/Ketone], \[Substituents\], **oxime**.
- *Examples:*
  - **1H-Pyrazole-4-carboxaldehyde, 1,3-dimethyl-, oxime**.
  - **2,7-Dioxatricyclo\[4.4.0.0(3,8)\]decan-4-one, oxime**.

### 194. Organometallic Compounds

Compounds containing metal-carbon bonds (excluding simple salts) are often named by the metal atom.

- *Example:* **Ferrocene**; **Stannane, tetrabutyl-**; **Silane, chlorotrimethyl-**.

### 196. Ethers

Named substitutively using *alkoxy-* prefixes.

- *Examples:* **Benzene, methoxy-** (Anisole); **Ethane, 1,1'-oxybis-** (Diethyl ether).

### 197. Phosphorus Compounds

Include Phosphines, Phosphonates, and Phosphates.

- *Examples:* **Phosphine, triphenyl-**; **Phosphonic acid, diethyl ester**.

### 198. Onium Compounds

Cations derived from heteroatoms.

- *Examples:* **Ammonium**; **Pyridinium**.

### 200. Sulfur Compounds

Includes Sulfides, Sulfoxides, Sulfones, and Sulfonamides.

- *Example (Sulfide):* **Benzene, (methylthio)-**.
- *Example (Sulfone):* **Benzene, (methylsulfonyl)-**.
- *Example (Sulfonamide):* **Benzenesulfonamide, 4-methyl-**.

---

## Stereochemistry and Stereoparents (¶202–212)

### 202. Stereoparents

Certain complex natural products (Terpenes, Steroids) have trivial names that imply a specific absolute configuration. These are used as Heading Parents.

- *Examples (Steroid):* **Cholestane**; **Androstane**; **Pregnane**.
- *Examples (Terpene):* **Pinane**; **Bornane**.

### 203. Stereochemical Descriptors

Stereochemical descriptors are used extensively and follow specific placement rules, often appearing at the end of the name for indexing, or preceding the substituent they modify.

- **(E)- / (Z)-**: Used for double bond isomers (Entgegen/Zusammen).
  - *Example:* **2-Butenoic acid, (E)-**.
- **cis- / trans-**: Used for ring substituents or double bonds.
  - *Example:* **Cyclohexanol, 4-methyl-, cis-**.
- **(R)- / (S)-**: Used for chiral centers (Cahn-Ingold-Prelog).
  - *Example:* **2-Butanol, (R)-**.
- **.alpha.- / .beta.-**: Used specifically in steroid and terpene nomenclature to denote stereochemistry relative to the plane of the ring system.
  - *Example:* **Cholestan-3-ol, (3.beta.)-**.
- **Carbohydrates:** Anomeric positions are designated with **.alpha.** or **.beta.**

### 206. Amino Acids and Peptides

Common amino acids retain their trivial names.

- *Examples:* **Alanine**; **Glycine**; **Leucine**.
- Derivatives are named as substituted acids or esters: **L-Alanine, methyl ester**.
- **Rule:** Amino acid residues are concatenated with hyphens.
- *Examples=:*
  - **Glycyl-dl-aspartic acid**.
  - **Glycylglycylglycylglycine**.

---

## Specialized Substances (¶213–224)

### 215. Coordination Compounds

The naming of transition metal complexes strictly follows the "Central Metal" heading convention.

- **Heading:** The name of the metal appears first.
- **Ligands:** Ligands follow the metal, separated by commas or parentheses.
- **Hapticity (.eta.):** Used when a ligand coordinates through contiguous atoms (e.g., pi-systems). Written as *.eta.* followed by the number of atoms.
- **Bridging (.mu.):** Used for ligands shared between two metal centers. Written as *.mu.*.
- *Examples:*
  - **Iron, tricarbonyl\[(1,2,3,4-.eta.)-1,3-cyclooctadiene\]-**.
  - **Tungsten, pentacarbonyl...**.
  - **Bis(tricarbonyliron)-(Fe-Fe), (.mu.-bromo) \[.mu.-.eta.-1:.eta.-2-2-(4-fluorophenyl)vinyl\]-** (Complex binuclear cluster).
  - **Manganese, acetylpentacarbonyl-**.

### 220. Isotopically Labeled Compounds

Compounds where specific atoms are replaced by isotopes.

- *Example:* **Methane-d3-ol** (Methanol with 3 Deuterium atoms); **Chlorobenzene-d5**.
- The isotope is indicated after the name of the part of the molecule it modifies.
- While mass numbers are typically used, the dataset specifically lists named isotopes as distinct entries.
  - *Example:* **Deuterium**.

### 223. Porphyrins

Macrocyclic compounds related to heme.

- *Example:* **21H,23H-Porphine**.

### 224. Vitamins

Specific headings are used for vitamins.

- *Example:* **Retinol** (Vitamin A); **Riboflavin**.
