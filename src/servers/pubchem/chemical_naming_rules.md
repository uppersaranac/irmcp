# Naming of Chemical Substances

---

## 1. Purpose and Scope

- The names are identify substances in the NIST Spectral Libraries.
- Every **unique chemical structure** receives one **unique name**.
- Unless using common names, names are **structure-based**, aiming for **consistency, uniqueness, and retrievability** in databases.

---

## 2. General Principles

1. **Common names First**  
   - We prefer names that are commonly used in the the analytical chemistry or biomedical literature.
   - **Example:**  
     - Common name: **acetone** not **propan-2-one**

2. **Uniqueness**
   - No two distinct structures should share the same name.
   - Stereoisomers, isotopologues, and salts each receive distinct names.

3. **Parent Selection**
   - The “parent” is the main structural moiety; all other features are described as modifications.
   - Parent choice depends on the importance of the moiety in chemical reactions compared to
     the other moeties in the structure:
     - Functional group priority
     - Ring vs. chain preference
     - Simplicity of substituent description

---

## 3. Selecting the Parent Structure

1. **Longest Chain or Preferred Ring**
   - For acyclic compounds: choose the longest continuous carbon chain containing the highest-priority group.
   - For cyclic/fused systems: use the **preferred ring system** used in the chemical literature.
   - If the ring system or the carbon chain has a common chemical name, prefer to use that name
     for the system or chain.
   - **Example:**  
     - Structure: 4-chlorohexan-2-one  
       - Longest chain with ketone: hexane → parent name = hexan-2-one.

2. **Numbering the Parent**
   - Number to give the lowest locants to:
     1. Principal functional group
     2. Multiple bonds
     3. Substituents
   - For heterocycles, number to give the lowest locants to heteroatoms.

3. **Parent Retention in Complex Structures**
   - In fused polycyclic systems, follow standard fixed numbering.
   - **Example:**  
     - *naphtho[2,1-b]thiophene* — numbering fixed by fusion rules.

---

## 4. Functional Group Priority for Suffix Use

Priority determines which group appears as the suffix (part of the parent name) vs. a prefix.  
Typical order (highest to lowest):

1. Carboxylic acids and derivatives (anhydrides, esters, acyl halides, amides)
2. Sulfonic acids and derivatives
3. Aldehydes
4. Ketones
5. Alcohols/phenols
6. Amines
7. Ethers
8. Halides

**Example:**  

- Structure: CH₃–CH₂–OH and CHO on the same chain.  
- Acid/aldehyde > alcohol → aldehyde is suffix: **3-hydroxypropanal**

---

## 5. Substituents

### 5.1 Simple Substituents

- Named as prefixes.
- Use hyphen between locant and substituent name.
- Multiplicative prefixes: di-, tri-, tetra-, etc.

**Example:**  

- 2-bromo-4-methylpentane  
  - Bromo and methyl substituents, numbered for lowest locants.

### 5.2 Complex Substituents

- If the substituent itself has branching, number and name it completely, then enclose in parentheses.

**Example:**  

- 3-(2-hydroxyethyl)hexan-1-ol

### 5.3 Order of Multiple Substituents

- Alphabetize by the first letter of the substituent name **ignoring multiplicative prefixes**.
- **Example:**  
  - 4-bromo-2-chlorohexane  
    - "bromo" comes before "chloro".

---

## 6. Multiple Bonds

- Double bonds take precedence over triple bonds in numbering.
- Indicate position with the lower-numbered carbon.
- **Example:**  
  - hex-2-en-4-yne

---

## 7. Stereochemistry

1. **Tetrahedral Centers**
   - Use **(R)** or **(S)** before the relevant part of the name.
   - Multiple centers: separate with commas inside one set of parentheses.
   - **Example:**  
     - (2R,3S)-butane-2,3-diol

2. **Double Bonds**
   - Use **(E)** / **(Z)** for stereodescriptors.
   - **Example:**  
     - (E)-hex-2-ene

3. **Cis/Trans**
   - Used only in specific cases (cyclic systems).

---

## 8. Ring Systems

### 8.1 Monocyclic

- Name from root indicating atom count, saturation, and heteroatoms.
- Number to give lowest locants to heteroatoms and substituents.
- **Example:**  
  - pyridine (heteroatom at position 1 by default)

### 8.2 Fused Systems

- Use fusion notation with square brackets and fixed numbering.
- **Example:**  
  - naphtho[1,2-b]thiophene

### 8.3 Spiro and Bridged Systems

- **Spiro:** spiro prefix + bracket with atom counts.
  - Example: spiro[4.5]decane
- **Bridged:** bicyclo or polycyclo with locant system.
  - Example: bicyclo[2.2.1]heptane

---

## 9. Isotopes, Charges, and Radicals

1. **Isotopes**
   - Mass number in square brackets before the element.
   - Example: [2H]ethanol

2. **Charges**
   - Charge in parentheses after atom.
   - Example: iron(3+)

3. **Radicals**
   - “yl” suffix for monovalent radicals.
   - Example: methyl (CH₃•) = methyl radical

---

## 10. Inorganic Compounds

- Cation first, anion second.
- Oxidation state in Roman numerals in parentheses.
- **Example:**  
  - cobalt(II) chloride

---

## 11. Salts, Solvates, and Mixtures

### 11.1 Salts

- Name cation first, then anion.
- Hydrates/solvates appended.
- Example: sodium sulfate decahydrate

### 11.2 Mixtures/UVCBs

- Name describes the source and composition.
- Example: “petroleum distillates, hydrotreated light”

### 11.3 Adducts

- Named as “compound A–compound B” with ratios if known.
- Example: 1:1 phenol–formaldehyde adduct

---

## 12. Formatting Rules

1. Hyphen between locant and name part.
2. Comma between locants.
3. No spaces except between separate words in trivial descriptors.
4. All lowercase except for proper names.

---

## 13. Worked Examples

1. **2-bromo-4-chlorophenol**
   - Phenol chosen as parent due to OH priority over halogens.
   - Halogens in alphabetical order: bromo before chloro.

2. **(E)-1,2-dichloroethene**
   - Parent = ethene.
   - Two chloro substituents at positions 1 and 2.
   - Double bond stereochemistry = E.

3. **sodium 4-nitrobenzoate**
   - Salt: cation (sodium) first.
   - Parent acid is benzoic acid; NO₂ at position 4.

4. **naphtho[2,1-b]thiophene**
   - Parent is fused naphthalene + thiophene.
   - Numbering fixed by CAS fusion scheme.
