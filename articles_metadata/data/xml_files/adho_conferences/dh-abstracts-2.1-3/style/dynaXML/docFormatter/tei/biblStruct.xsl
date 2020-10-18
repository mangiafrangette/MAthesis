<xsl:stylesheet xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:eg="http://www.tei-c.org/ns/Examples"
    xmlns:xdoc="http://www.pnp-software.com/XSLTdoc" exclude-result-prefixes="#all"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.w3.org/1999/xhtml">



    <!-- Check for single or double quotation mark format -->
    
    <xsl:param name="quotation_format" as="xs:string">
        <xsl:value-of select="TEI/teiHeader/encodingDesc/editorialDecl/quotation//*[@xml:id='quotation_format']"/>
    </xsl:param>
    

    <xdoc:doc>divisions</xdoc:doc>
    <xsl:template match="div|div0|div1|div2|div3|div4|div5|div6">
        <xsl:variable name="depth">
            <xsl:apply-templates select="." mode="depth"/>
        </xsl:variable>
        <div>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="concat('teidiv',$depth)"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:call-template name="rend"/>
            <xsl:apply-templates/>
        </div>
    </xsl:template>


    <xdoc:doc>divisions mode="depth". Returns the hierarchical level of the division, starting from
        0.</xdoc:doc>
    <xsl:template match="div|div0|div1|div2|div3|div4|div5|div6" mode="depth">
        <xsl:choose>
            <xsl:when test="name(.) = 'div'">
                <xsl:value-of select="count(ancestor::div)"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:choose>
                    <xsl:when test="ancestor-or-self::div0">
                        <xsl:value-of select="substring-after(name(.),'div')"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="number(substring-after(name(.),'div')) - 1"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="head" mode="plain">
        <xsl:apply-templates/>        
    </xsl:template>


    <xsl:template match="ab">
        <div>
            <xsl:call-template name="atts"/>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="p">
        <span>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'p'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:call-template name="rend"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>


    <!-- named templates -->

    
    <xsl:template name="rendition">
        <xsl:param name="defaultRend"/>
        <xsl:choose>
            <xsl:when test="@rendition and @rendition != ''">
                <xsl:attribute name="class">
                    <xsl:choose>
                        <xsl:when test="$defaultRend != ''">
                            <xsl:value-of select="concat($defaultRend,' ',translate(normalize-space(@rendition), '#', ''))"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="translate(normalize-space(@rendition), '#', '')"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:attribute>
                
            </xsl:when>
            <xsl:otherwise>
                
                <xsl:if test="$defaultRend !=''">
                    <xsl:attribute name="class">
                        <xsl:value-of select="$defaultRend"/>
                    </xsl:attribute>
                    
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    
    <xsl:template name="rend">
        <xsl:if test="@rend and @rend != ''">
        <xsl:attribute name="style">
            <xsl:value-of select="@rend"/>
        </xsl:attribute>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="atts">
        <xsl:call-template name="id"/>
        <xsl:call-template name="rendition"/>
        <xsl:call-template name="rend"/>
    </xsl:template>
    
  

    <xdoc:doc>Passes xml:id from TEI element to corresponding XHTML element.</xdoc:doc>
    <xsl:template name="id">
        <xsl:if test="@xml:id">
            <xsl:attribute name="id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>


    <xdoc:doc>Do nothing by default with teiHeader, so elements can be accessed explicitly
        elsewhere.</xdoc:doc>
    <xsl:template match="teiHeader"/>

    <!-- drama -->
    <xsl:template match="sp">
        <div>
            <xsl:call-template name="rendition"/>
            <xsl:call-template name="id"/>
            <xsl:apply-templates/>
        </div>
    </xsl:template>




    <xdoc:doc>Handling of poetic stanzas. Special case for lg[@rend='sublg'], which represents a
        "line group" within a stanza, that is not separated by white space from the recent of the
        stanza, e.g., the octect and sestet within a Petrarchan sonnet or the four quatrains and
        couplet in a Shakesperian sonnet.</xdoc:doc>

    <xsl:template match="lg">
        <span>
            <xsl:choose>
                <xsl:when test="contains(@rendition,'sublg')">
                    <xsl:call-template name="rendition"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="rendition">
                        <xsl:with-param name="defaultRend">lg</xsl:with-param>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <xsl:apply-templates select="head" mode="lgHead"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="head" mode="lgHead">
        <span>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'genericHeading'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:call-template name="id"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="lg/head"/>

    <xsl:template match="l">
        <span class="lineWrapper">
            <span>
                <xsl:attribute name="class">
                    <xsl:choose>
                        <xsl:when test="label">
                            <xsl:text>lineWithLabel</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>line</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:attribute>
                <span>
                    <xsl:call-template name="id"/>
                    <xsl:call-template name="rend"/>
                    <xsl:attribute name="class">
                        <xsl:choose>
                            <xsl:when test="not(contains(@rendition,'ti-'))">
                                <xsl:call-template name="rendition">
                                    <xsl:with-param name="defaultRend">
                                        <xsl:value-of select="'ti-0'"/>
                                    </xsl:with-param>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:call-template name="rendition"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </span>
            </span>
            <xsl:if test="label">
                <span class="lineLabel">
                    <xsl:apply-templates select="./label" mode="lineLabel"/>
                </span>
            </xsl:if>
        </span>
    </xsl:template>


    <xsl:template match="l/label"/>
    
    <xsl:template match="l/label" mode="lineLabel">
        <xsl:apply-templates/>
    </xsl:template>


    <xsl:template match="note">
        <span>
            <xsl:call-template name="atts"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="note" mode="hide">
        <div>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'note suppress'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:apply-templates/>
        </div>
    </xsl:template>


    <xsl:template match="note[@type= 'gloss']" priority="1">
        <xsl:apply-templates select="." mode="generated-reference"/>
    </xsl:template>

    <xsl:template match="note[@type = 'gloss']/term">
        <span class="glossTerm">
            <xsl:apply-templates/>
        </span>
    </xsl:template>


    <xsl:template match="note[@type = 'gloss']/gloss">
        <span class="gloss">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="note[@type = 'dev']|note[@type = 'metadocument']"/>

   <!-- jsInit not needed if use window.onload in .js file -->
    <xsl:template name="jsInit">
        <xsl:attribute name="onload">
            <xsl:value-of select="'Tooltip.init();'"/>
        </xsl:attribute>
    </xsl:template>


    <xsl:template match="listBibl">
        <div>
            <xsl:call-template name="atts"/>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- need similar for biblStruct and biblFull -->
    <xsl:template match="listBibl/bibl">
        <div>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'bibl'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <xsl:template match="listBibl/biblStruct">
        <div>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'bibl'"/>
                </xsl:with-param>
            </xsl:call-template>
         <!--   <xsl:call-template name="get-author"/> -->
        <!--    <xsl:call-template name="get-editor-analytic"/> -->
            <xsl:if test="analytic/title">
                <xsl:call-template name="get-biblScope"/>
            </xsl:if>
            <xsl:call-template name="get-title-monogr"/>
       <!--     <xsl:if test="analytic and not(analytic/author)">
                <xsl:call-template name="get-author-monogr"/>
            </xsl:if> -->
            
         <!--   <xsl:call-template name="get-editor-monogr"/> -->
         <!--   <xsl:call-template name="get-extent"/> -->
            <xsl:call-template name="get-pubPlace"/>
            <xsl:call-template name="get-publisher"/>
         <!--   <xsl:call-template name="get-date"/> -->
        </div>
    </xsl:template>
    
    <xsl:template name="get-author">
        <xsl:param name="author">
            <xsl:choose>
                <xsl:when test="analytic">
                    <xsl:choose>
                         <xsl:when test="analytic/author">
                             <xsl:value-of select="analytic/author"/>
                          </xsl:when>
                    </xsl:choose>
                </xsl:when>    
                <xsl:otherwise>
                    <xsl:choose>
                            <xsl:when test="monogr/author">
                                <xsl:value-of select="monogr/author"/>
                             </xsl:when>
                            <xsl:when test="analytic/editor"/>
                            <xsl:when test="monogr/editor"/>
                        <xsl:otherwise>
                             <xsl:value-of select="'unknown'"/>
                          </xsl:otherwise>
                 </xsl:choose>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:param>
        <xsl:if test="$author != ''">
            <xsl:choose>
                <xsl:when test="not(ends-with(normalize-space($author),'.'))">
                    <xsl:value-of select="concat(normalize-space($author),'. ')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat(normalize-space($author),' ')"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="get-author-monogr">
        <xsl:param name="author">
            <xsl:choose>
                        <xsl:when test="mongr/author/persName">
                            <xsl:value-of select="mongr/author/persName"/>
                        </xsl:when>
                        <xsl:when test="monogr/author">
                            <xsl:value-of select="monogr/author"/>
                        </xsl:when>
                <xsl:when test="analytic/editor"/>
                <xsl:when test="monogr/editor"/>
                        <xsl:otherwise>
                            <xsl:value-of select="'unknown'"/>
                        </xsl:otherwise>
                    </xsl:choose>
        </xsl:param>
        <xsl:if test="$author != ''">
            <xsl:choose>
                <xsl:when test="not(ends-with(normalize-space($author),'.'))">
                    <xsl:value-of select="concat('By ', normalize-space($author),'. ')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat('By ', normalize-space($author),' ')"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="get-editor-analytic">
        <xsl:param name="editor">
            <xsl:choose>
                <xsl:when test="analytic/editor">
                    <xsl:value-of select="analytic/editor"/><xsl:text>, ed. </xsl:text>
                </xsl:when>
                <!--
                    <xsl:when test="/TEI/teiHeader/fileDesc/sourceDesc/biblStruct/monogr/editor/persName/@key">
                    <xsl:call-template name="getXtmName">
                    <xsl:with-param name="target" select="/TEI/teiHeader/fileDesc/editor/author/persName/@key"/>
                    </xsl:call-template>
                    </xsl:when>
                -->
            </xsl:choose>
        </xsl:param>
        <xsl:if test="$editor != ''">
            <xsl:value-of select="concat(normalize-space($editor),', ed. ')"/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="get-editor-monogr">
        <xsl:param name="editor">
            <xsl:choose>
                <xsl:when test="monogr/editor">
                    <xsl:value-of select="monogr/editor"/>
                </xsl:when>
                <!--
                    <xsl:when test="/TEI/teiHeader/fileDesc/sourceDesc/biblStruct/monogr/editor/persName/@key">
                    <xsl:call-template name="getXtmName">
                    <xsl:with-param name="target" select="/TEI/teiHeader/fileDesc/editor/author/persName/@key"/>
                    </xsl:call-template>
                    </xsl:when>
                -->
            </xsl:choose>
        </xsl:param>
        <xsl:if test="$editor != ''">
            <xsl:value-of select="concat('Ed. ',normalize-space($editor),'. ')"/>
        </xsl:if>
    </xsl:template>

    <!--<xsl:template name="get-extent">
        <xsl:param name="extent" select="normalize-space(monogr/extent)"/>
        <xsl:if test="$extent != ''">
            <xsl:choose>
                <xsl:when test="ends-with($extent,'.')">
                    <xsl:value-of select="concat($extent,' ')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat($extent,'. ')"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template> -->
    
    <xsl:template name="get-biblScope">
        <xsl:variable name="refIdwHash">
            <xsl:value-of select="following-sibling::tei:monogr/tei:ref/@target"/>
        </xsl:variable>
        <xsl:variable name="refId">
            <xsl:value-of select="substring-after($refIdwHash, '#')"/>
        </xsl:variable>
        <xsl:apply-templates/>
        <xsl:if test="not(following-sibling::tei:monogr/tei:title[@level='m']) and $refId!=''">
            <xsl:text> </xsl:text>
            <xsl:if test="following-sibling::tei:monogr/tei:imprint/tei:date">
                <xsl:value-of select="following-sibling::tei:monogr/tei:imprint/tei:date"/>
                <xsl:text>. </xsl:text>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[1]">
                    <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[1], ',')"/>
                </xsl:when>
                <xsl:when test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][1]">
                    <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][1], ',')"/>
                </xsl:when>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[3]">
                    <xsl:text>, </xsl:text>
                    <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[2], ',')"/>
                    <xsl:text>, and </xsl:text>
                </xsl:when>
                <xsl:when test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][3]">
                    <xsl:text>, </xsl:text>
                    <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][2], ',')"/>
                    <xsl:text>, and </xsl:text>
                </xsl:when>
                <xsl:when test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[2]">
                    <xsl:text> and </xsl:text>
                    <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[2], ',')"/>
                </xsl:when>
                <xsl:when test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][2]">
                    <xsl:text> and </xsl:text>
                    <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][2], ',')"/>
                </xsl:when>
            </xsl:choose>
            <xsl:if test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[3]">
                <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:author[3], ',')"/>
            </xsl:if>
            <xsl:if test="ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][3]">
                <xsl:value-of select="substring-before(ancestor::tei:listBibl/tei:biblStruct[@xml:id=$refId]/tei:monogr/tei:editor[@role='editor'][3], ',')"/>
            </xsl:if>
            <xsl:text> </xsl:text>
            <xsl:value-of select="following-sibling::tei:monogr/tei:imprint/tei:biblScope[@type='pp']"/>
            <xsl:text>. </xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template name="get-title-monogr">
        <xsl:choose>
            <xsl:when test="preceding-sibling::tei:analytic">
                <xsl:choose>
                    <xsl:when test="tei:author = parent::tei:biblStruct/tei:analytic/tei:author">
                        <xsl:if test="tei:author[2]">
                            <xsl:apply-templates select="tei:author"/><xsl:text>, </xsl:text>
                        </xsl:if>
                        <xsl:apply-templates select="tei:title"/>
                        <xsl:if test="tei:edition"><xsl:apply-templates select="tei:edition"/></xsl:if>
                        <xsl:apply-templates select="tei:editor[@role='editor']"/>
                        <xsl:if test="tei:editor[@role='translator']">
                            <xsl:apply-templates select="tei:editor[@role='translator']"/>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="tei:author"/>
                        <xsl:apply-templates select="tei:title"/>
                        <xsl:if test="tei:edition"><xsl:apply-templates select="tei:edition"/></xsl:if>
                        <xsl:apply-templates select="tei:editor[@role='editor']"/>
                        <xsl:if test="tei:editor[@role='translator']">
                            <xsl:apply-templates select="tei:editor[@role='translator']"/>
                        </xsl:if>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="tei:editor[@role='editor'] and not(preceding-sibling::tei:analytic) and not(tei:author)">
                <xsl:apply-templates select="tei:editor[@role='editor']"/>
                <xsl:apply-templates select="tei:title"/>
                <xsl:if test="tei:edition"><xsl:apply-templates select="tei:edition"/></xsl:if>
                <xsl:if test="tei:editor[@role='translator']">
                    <xsl:apply-templates select="tei:editor[@role='translator']"/>
                </xsl:if>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="tei:author"/>
                <xsl:apply-templates select="tei:title"/>
                <xsl:if test="tei:edition"><xsl:apply-templates select="tei:edition"/></xsl:if>
                <xsl:apply-templates select="tei:editor[@role='editor']"/>
                <xsl:if test="tei:editor[@role='translator']">
                    <xsl:apply-templates select="tei:editor[@role='translator']"/>
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
        <!--    <xsl:when test="*//tei:ref/@target and not(contains(*//tei:ref/@target, '#'))">
                <xsl:if test="tei:imprint/tei:date[@type='update']"><xsl:value-of select="tei:imprint/tei:date[@type='update']"/></xsl:if>
            </xsl:when> -->
            <xsl:when test="ancestor-or-self::tei:biblStruct/*/tei:title/@level='u'">
                <xsl:value-of select="tei:imprint"/>
            </xsl:when>
            <xsl:when test="tei:title/@level='m'">
                <xsl:if test="tei:imprint/tei:biblScope/@type='vol'">
                    <xsl:value-of select="tei:imprint/tei:biblScope[@type='vol']"/>. </xsl:if>
                <xsl:choose>
                    <xsl:when test="tei:imprint/tei:pubPlace"><xsl:value-of select="tei:imprint/tei:pubPlace"/>: </xsl:when>
                    <xsl:otherwise>[n.p.]: </xsl:otherwise>
                </xsl:choose>
                <xsl:choose>
                    <xsl:when test="tei:imprint/tei:publisher"><xsl:value-of select="tei:imprint/tei:publisher"/>, </xsl:when>
                    <xsl:otherwise>[n.p.], </xsl:otherwise>
                </xsl:choose>
                <xsl:choose>
                    <xsl:when test="tei:imprint/tei:date"><xsl:value-of select="tei:imprint/tei:date"/>. </xsl:when>
                    <xsl:otherwise>[n.d.]  </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="tei:title/@level='j'">
                <xsl:if test="tei:imprint/tei:biblScope/@type='vol'"><xsl:value-of select="tei:imprint/tei:biblScope[@type='vol']"/></xsl:if>
                <xsl:if test="tei:imprint/tei:biblScope/@type='no'"><xsl:text>.</xsl:text><xsl:value-of select="tei:imprint/tei:biblScope[@type='no']"/></xsl:if>
               <!-- <xsl:if test="tei:imprint/tei:date"><xsl:text>&#10;</xsl:text>(<xsl:value-of select="tei:imprint/tei:date"/>)</xsl:if> -->
                <xsl:if test="tei:imprint/tei:biblScope/@type='pp'">: <xsl:value-of select="tei:imprint/tei:biblScope[@type='pp']"/></xsl:if>
                <xsl:text>. </xsl:text>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="get-pubPlace">
        <xsl:if test="monogr/imprint/pubPlace">
            <xsl:value-of select="concat(normalize-space(monogr/imprint/pubPlace),': ')"/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="get-publisher">
        <xsl:choose>    
        <xsl:when test="monogr/imprint/publisher">
            <xsl:value-of select="concat(normalize-space(monogr/imprint/publisher),' ')"/>
        </xsl:when>
        </xsl:choose>
    </xsl:template>
    
   <!-- <xsl:template name="get-date">
    <xsl:if test="monogr/imprint/date/@when">,
                    <xsl:value-of select="normalize-space(monogr/imprint/date/@when),'. '"/>
       </xsl:if>
    </xsl:template> -->
    
    <xsl:template match="biblStruct">
        <span>
            <xsl:call-template name="atts"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
    <!-- ADHO special case type book -->
    <xsl:template match="biblStruct [@type='book']">
                <xsl:apply-templates select="get-author"/>
                <xsl:if test="tei:title/@level='m'">
                    <xsl:apply-templates select="get-title-monogr" />
                </xsl:if>
    </xsl:template>
    
    
    <xsl:template match="lb">
        <br>
        <xsl:call-template name="rendition"/>
        <xsl:call-template name="id"/>
        </br>
    </xsl:template>
    
    
    <xsl:template match="note[@type = 'chronoLetter']" priority="200">
        <!--
        <div>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend" select="'chronoLetter'"/>
            </xsl:call-template>
            <h1 style="font-style:italic;font-weight:500;letter-spacing:3px;font-size:120%;">From a letter:</h1>
            <xsl:apply-templates/>
        </div>
        -->
        <ul><li>
            <xsl:value-of select="concat('From a letter: ',cit/bibl/title[@level = 'a'])"/>
            <span>
                <xsl:attribute name="class" select="concat('showTip ',@xml:id)"/>
                <span class="ref">  </span>
            </span></li>
        </ul>
        <span style="display:none;">
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend" select="'chronoLetter'"/>
            </xsl:call-template>    
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
    
    
    
    <xsl:template match="castItem[parent::castList[contains(@rendition,'#list')]]">
        <span>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'castItem'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
                      
    <!-- cit w/ block quote and block bibl, as commonly found in epigraphs. -->
    <xsl:template match="cit/quote[contains(@rendition, '#block') and following-sibling::bibl]|cit/quote[contains(@rendition, '#block') and following-sibling::bibl]/lg">
        <div>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'epiblock'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    
    <!--
    
    <xsl:template match="cit[contains(@rendition,'#block')]">
        <span>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend">
                    <xsl:value-of select="'blockquote'"/>
                </xsl:with-param>
            </xsl:call-template>
            <xsl:call-template name="rend"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    -->
    
    <!-- assumes epigraphs are block elements by default -->
    <!-- Template below was throwing ambiguous rule error, and the template itself doesn't appear to be necessary.  Not sure why I 
    wrote it in the first place.-->
    <!--
    <xsl:template match="cit[contains(@rendition,'#block')]/quote|epigraph/cit/quote">
        <span>
           <xsl:call-template name="rendition"/>
           <xsl:call-template name="id"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    -->
 
    
        
    <xsl:template match="/TEI/teiHeader/fileDesc/titleStmt/title">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="figure">
        <div>
            <xsl:call-template name="atts"/>
           <!-- <xsl:apply-templates/> -->
            <xsl:apply-templates select="graphic"/>
            <xsl:apply-templates select="head" mode="caption"/>
        </div>
    </xsl:template>
        
    <xsl:template match="graphic">
        <a href="{@url}">
        <img>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <xsl:call-template name="rendition">
                <xsl:with-param name="defaultRend" select="'figure'"/>
            </xsl:call-template>
            <xsl:attribute name="src">
                <xsl:value-of select="@url"/>
            </xsl:attribute>
            <xsl:attribute name="alt">
                <xsl:choose>
                    <xsl:when test="../figDesc">
                        <!--
                        <xsl:value-of select="normalize-space(../figDesc/text())"/>
                        -->
                        <xsl:apply-templates mode="alt" select="../figDesc"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="'graphic'"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
        </img>
        </a>
    </xsl:template>
    
    <xsl:template match="figDesc//*" mode="alt">
        <xsl:value-of select="."/>
    </xsl:template>
    
    
    <xsl:template match="graphic[@mimeType = 'application/x-shockwave-flash']">
        <xsl:param name="width">
            <xsl:value-of select="substring-before(@width,'px')"/>
        </xsl:param>
        <xsl:param name="height">
            <xsl:value-of select="substring-before(@height,'px')"/>
        </xsl:param>
        <object>
            <xsl:if test="@width and @width != ''">
                <xsl:attribute name="width">
                    <xsl:value-of select="$width"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@height and @height != ''">
                <xsl:attribute name="height">
                    <xsl:value-of select="$height"/>
                </xsl:attribute>
            </xsl:if>
            <param name="movie" value="{@url}"/>
            <embed src="{@url}">
                <xsl:if test="@width and @width != ''">
                    <xsl:attribute name="width">
                        <xsl:value-of select="$width"/>
                    </xsl:attribute>
                </xsl:if>
                <xsl:if test="@height and @height != ''">
                    <xsl:attribute name="height">
                        <xsl:value-of select="$height"/>
                    </xsl:attribute>
                </xsl:if>
            </embed>
        </object>
    </xsl:template>

    <xsl:template match="figure/head"/>
    
    
    <xsl:template match="lg/l[position() = 1]//q[@prev and not(cdext)]" priority="10">
        <xsl:param name="rendition">
            <xsl:value-of select="translate(translate(normalize-space(@rendition), '#sq', ''), '#dq', '')"/>
        </xsl:param>
        <span>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <!-- insteading of calling "rendition" template, need to remove #sq -->
            <xsl:if test="$rendition != ''">
                <xsl:attribute name="class">
                    <xsl:value-of select="translate(normalize-space($rendition), '#', '')"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="contains(@rendition,'#sq')">
                    <xsl:text>‘</xsl:text>
                </xsl:when>
                <xsl:when test="contains(@rendition,'#dq')">
                    <xsl:text>“</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:choose>
                        <xsl:when test="$quotation_format = 'single'">
                            <xsl:text>‘</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>“</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates/>
            <xsl:choose>
                <xsl:when test="contains(@rendition,'#sq')">
                    <xsl:text>’</xsl:text>
                </xsl:when>
                <xsl:when test="contains(@rendition,'#dq')">
                    <xsl:text>”</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:choose>
                        <xsl:when test="$quotation_format = 'single'">
                            <xsl:text>’</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>”</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    
    <xsl:template match="q[@next and @prev]">
        <xsl:param name="rendition">
            <xsl:value-of select="translate(translate(normalize-space(@rendition), '#sq', ''), '#dq', '')"/>
        </xsl:param>
        <span>
            <xsl:call-template name="id"/>
            <xsl:call-template name="rend"/>
            <!-- insteading of calling "rendition" template, need to remove #sq -->
            <xsl:if test="$rendition != ''">
                <xsl:attribute name="class">
                    <xsl:value-of select="translate(normalize-space($rendition), '#', '')"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </span>
    </xsl:template>


    <!-- pb -->
    
    <xsl:template match="pb[@facs = 'dummy']"/>
    
    <xsl:template name="pb-handler">
        <xsl:param name="pn"/>
        <xsl:param name="page-id"/>
        
        <span class="page-num">
            <xsl:call-template name="atts"/>
            <span class="pbNote">page: </span>
            <xsl:value-of select="@n"/>
            <xsl:text> </xsl:text>
        </span>
    </xsl:template>
   
    <xsl:template match="pb">        
        <xsl:param name="pn">
            <xsl:number count="//pb" level="any"/>    
        </xsl:param>
    </xsl:template>
    <xsl:template match="fw">
        <span>
            <xsl:call-template name="rendition"/>
            <xsl:call-template name="id"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
             
      
    
    <!-- using parse date in old TEI version when format was YYYYMMDD, without hyphens -->
    <!--
<xsl:template name="parse-date">
    <xsl:param name="date"/>
    <xsl:value-of select="concat(substring($date,1,4),'-',substring($date,5,2),'-',substring(@when,6,2))"/>
</xsl:template>
-->
    
<!-- date just copied from P4, need to clean up -->
    <xsl:template match="date">
                    <xsl:call-template name="atts"/>
                <xsl:choose>
                    <!-- if date or dateRange is empty, then display @value or @from and @to -->
                    <xsl:when test="not(child::*) and not(text())">
                        <xsl:choose>
                            <xsl:when test="name() = 'date'">
                                <xsl:value-of select="@when"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="@from"/><xsl:text> &#x2014; </xsl:text><xsl:value-of select="@to"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates/>
                    </xsl:otherwise>
                </xsl:choose>
    </xsl:template>

<xsl:template match="ab[@type = 'exam-answer']">
<span class="exam-answer"/>
</xsl:template>
    
    
    <xsl:template match="*[@sameAs]" priority="10">
        <xsl:param name="id" select="substring-after(@sameAs,'#')"/>
        <xsl:apply-templates select="//*[@xml:id = $id]"/>
    </xsl:template>
    
    <xsl:template match="note[@type = 'metadata']"/>

    <!-- utterance -->
    <xsl:template match="u">
        <div>
            <strong>
                <xsl:apply-templates select="id(substring-after(@who,'#'))"/>
            </strong>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- suppressed elements -->
    <xsl:template match="fw[@type = 'header']"/>

</xsl:stylesheet>