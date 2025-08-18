# PUG View

PUG View is a REST-style web service that provides information content that is not directly contained within the primary PubChem Substance, Compound, or BioAssay records. Its purpose is primarily to drive the PubChem database summary record web pages, but can also be used independently as a programmatic web service.

PUG View is mainly designed to provide complete summary reports on individual PubChem records. Users may also be interested in [PUG REST](pug-rest-tutorial.md), a different style of service that gives smaller bits of information about one or more PubChem records.

**503 HTTP STATUS CODE**:  Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

## Formats

PUG View provides structured information in a variety of formats, specified at the end of the URL path. Most results can be formatted as JSON(P), XML, or ASN.1 as text (ASNT) or base64-encoded binary (ASNB). For example, these all contain exactly the same information, just in different formats:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON)

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSONP?callback=func](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSONP?callback=func)

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/XML](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/XML)

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/ASNT](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/ASNT)

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/ASNB](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/ASNB)

An XML schema is available here. Note that the JSON and ASN.1 formats follow the same content model.

[https://pubchem.ncbi.nlm.nih.gov/pug_view/pug_view.xsd](https://pubchem.ncbi.nlm.nih.gov/pug_view/pug_view.xsd)

## Record Summaries

### Full Records and Indexes

PUG View provides record summaries for the three primary PubChem databases - Compounds, Substances, and BioAssays - as well as patents and targets. Each of these can be accessed as an index, providing a listing of what information is present, but without the entire data content; essentially a table of contents for that record:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/index/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/index/compound/1234/JSON)

Or the complete data can be retrieved:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON)

This choice of index or full data is applicable to all the primary record types.

### Specific Heading

If only a subcategory of information is desired, a heading can be used to restrict the data returned. Note that the index as above is a convenient way to see what headings are present for a given record, as not all records will have all possible headings present. For example, to get just the experimental property section:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON?heading=Experimental+Properties](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON?heading=Experimental+Properties)

Or even just a single value type, like melting point:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON?heading=Melting+Point](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON?heading=Melting+Point)

Section headings that can be used in PUG-View data retrieval can be found in the PubChem Compound TOC tree (using the PubChem Classification Browswers).

[https://pubchem.ncbi.nlm.nih.gov/classification/#hid=72](https://pubchem.ncbi.nlm.nih.gov/classification/#hid=72)  
 

### Compounds

Compounds records are accessed by CID number. Note that PUG View provides textual and third-party information associated with the compound, but not the chemical structure, which is handled by other PubChem services.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON)

### Substances

Substances records are accessed by SID number. Information on substances is fairly minimal; in particular, no third party annotation is associated with substances. Again, chemical structure is not part of PUG View’s results.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/1/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/1/JSON)

### BioAssays

BioAssays are accessed by AID number.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/assay/1/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/assay/1/JSON)

### Patents

Patents can be accessed by an identifier string.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/US-5837728-A/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/US-5837728-A/JSON)

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/US-2015000048-A1/XML](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/US-2015000048-A1/XML)

### Genes

Gene information can be retrieved by NCBI Gene ID:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/gene/1/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/gene/1/JSON)

### Proteins

Protein information can be retrieved by NCBI Protein Accession:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/protein/P00533/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/protein/P00533/JSON)

### Pathways

Pathway information can be retrieved by Source:ExternalID:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/pathway/Reactome:R-HSA-70171/JSON/](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/pathway/Reactome:R-HSA-70171/JSON/)

### Taxonomies

Taxonomy information can be retrieved by NCBI Taxonomy ID:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/taxonomy/9606/JSON/](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/taxonomy/9606/JSON/)

### Cell Lines

Taxonomy information can be retrieved by Cell Line name (case-insensitive):

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/cell/HeLa/JSON/](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/cell/HeLa/JSON/)

### Elements

Element information can be retrieved by atomic number:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/element/17/JSON/](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/element/17/JSON/)

## Special Reports

The following are not primary PubChem records, but rather extra information of various sorts that is attached to PubChem records. These reports contain information not present in the main record data described above.

### Annotations

PUG View can provide information of a specific type across all of PubChem’s primary databases. For example, if you are interested in all of the experimental viscosity measurements contained within PubChem and its associated third-party annotations, you can request this by heading:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/Viscosity/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/Viscosity/JSON)

Or equivalently (useful if the heading contains special characters not compatible with URL syntax):

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/JSON?heading=Viscosity](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/JSON?heading=Viscosity)

This will include PubChem identifiers – CIDs in this example – for each data value, along with attribution detailing exactly where each bit of information was obtained.

Note that in [the PubChem data model](data-model-change-2019.md), a heading may refer to different types of PubChem records, making it necessary to specify which one is intended:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/Boiling%20Point/XML?heading_type=Compound](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/Boiling%20Point/XML?heading_type=Compound)

Also keep in mind that some headings have more data than others, and retrieval is limited. There will be "Page" and "TotalPages" values at the end of the request data, that will indicate the given page number and whether there is more data than shown in the given request (that is, whether TotalPages is greater than one). By default, page #1 is returned, but subsequent pages (up to the TotalPages limit) can be accessed by adding a page argument: 

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/CAS/JSON?page=10](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/CAS/JSON?page=10)

Lastly, it is possible to get a complete list of all annotation headings (and their types) for which PubChem has any data, and that can be used in URLs such as the above:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug/annotations/headings/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug/annotations/headings/JSON)

### Source Categories

PUG View can list all PubChem depositors and their SIDs for a given compound, including a categorization of each source – such as chemical vendor, research and development, journal publishers, etc.:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/1234/JSON)

### Literature

This will give URLs into PubMed for literature associated with a compound, organized by subheading:

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/literature/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/literature/compound/1234/JSON)

### Biologics

This is used do display biologic images associated with compounds. The integer here is an internal identifier, which will be present in the primary compound record.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/image/biologic/243577/SVG](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/image/biologic/243577/SVG)

### QR

This is a specialized image generator for QR codes that link to the LCSS page for a compound, intended for safety and hazard labelling.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/qr/short/compound/1234/SVG](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/qr/short/compound/1234/SVG)

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/qr/long/compound/1234/SVG](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/qr/long/compound/1234/SVG)

### Linkout

This gives a listing of all the NCBI LinkOut records present for a substance, compound, or assay.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/linkout/compound/1234/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/linkout/compound/1234/JSON)

### PDB/MMDB Structures

This gives a listing of 3D protein structures associated with a compound. 

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/structure/compound/2244/JSON](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/structure/compound/2244/JSON)

### Annotation Attachments

This is another specialized retrieval for attachments associated with some records, such as spectral images, etc. This key value will be present in the main record.

[https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/key/236678_1](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/key/236678_1)

## Limitations

* Some users are often confused with PUG-View and PUG-REST.  While PUG-REST retrieves property values computed by PubChem, PUG-View retrieves annotations collected from other data sources. 
* Contrary to PUG-REST, PUG-View takes only CID (rather than chemical names, InChIKeys or other identifiers). Therefore, to get annotations corresponding to non-CID identifiers, they need to be converted to CIDs first and then those CIDs should be used in PUG-View requests.
* Another important difference between PUG-REST and PUG-View is that PUG-View cannot take multiple CIDs in a single request, whereas PUG-REST can. That is, of the following two PUG-View requests, only the first one will work:
    
    **(Correct)** [https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1/JSON?heading=Substances+by+Category](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1/JSON?heading=Substances+by+Category)
    
    **(Incorrect)** [https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1,2,3/JSON?heading=Substances+by+Category](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1,2,3/JSON?heading=Substances+by+Category)
