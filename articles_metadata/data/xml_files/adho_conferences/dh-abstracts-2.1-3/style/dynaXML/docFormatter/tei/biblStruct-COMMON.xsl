<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
  xmlns:ns="http://www.tei-c.org/ns/1.0" 
  xmlns:date="http://exslt.org/dates-and-times"
  xmlns:parse="http://cdlib.org/xtf/parse"
  xmlns:xtf="http://cdlib.org/xtf"
  xmlns:session="java:org.cdlib.xtf.xslt.Session"
  xmlns:editURL="http://cdlib.org/xtf/editURL"
  xmlns:FileUtils="java:org.cdlib.xtf.xslt.FileUtils"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  extension-element-prefixes="date FileUtils"
  exclude-result-prefixes="#all">
 <!-- Bibliographical renderings -->

  <xsl:template match="listBibl/biblStruct">
    <div>
      <xsl:value-of select="'bibl'"/> 
      <xsl:apply-templates/>
    </div>
  </xsl:template>

 <xsl:template match="biblStruct">
  <p style="text-indent:-10mm;margin-left:10mm">
   <xsl:if test="@n">
    <span style="font-weight:bold;margin-left:2mm">
     <xsl:value-of select="@n"/>
     <xsl:text>-&#x09;</xsl:text>
    </span>
   </xsl:if>
   <xsl:apply-templates/>
  </p>

 </xsl:template>

 <xsl:template match="analytic">

  <xsl:apply-templates select="author"/>
  <xsl:apply-templates select="title"/>

 </xsl:template>


 <xsl:template match="monogr">

  <xsl:apply-templates select="author"/>
  <xsl:apply-templates select="editor"/>
  <xsl:apply-templates select="title"/>
  <xsl:apply-templates select="imprint"/>
 </xsl:template>


 <xsl:template match="monogr[@rend]">
  <xsl:variable name="monogrnote" select="@rend"/>
  <xsl:value-of select="$monogrnote"/>
  <xsl:text> </xsl:text>
  <xsl:apply-templates/>
 </xsl:template>

 <xsl:template match="imprint[@rend]">
  <xsl:variable name="imprintnote" select="@rend"/> [<xsl:value-of select="$imprintnote"
  /><xsl:text>: </xsl:text><xsl:apply-templates/>] </xsl:template>

  <xsl:template match="author">
    
    <!-- MB 2003-08-01 
      
** If our author name is the same as the
     preceding one, output a string of dashes in its place. NB
     this presupposes that identical names are indeed entered
     identically! It might also be a wise precaution to
     normalize-space both the string values we are
     comparing. Also, the "suppression marker" perhaps ought to
     be in a variable rather than hard-coded as here.
-->
    
    <xsl:variable name="fname" select="child::forename"/>
    
    
    <xsl:choose>
      <xsl:when
        test="preceding::biblStruct[1]/*/editor[1] = . or preceding::biblStruct[1]/*/author[1] = .">
        <xsl:choose>
          
          <xsl:when test="preceding::bibl[1]/author = .">
            <xsl:text>----.&#160;</xsl:text>
          </xsl:when>
          <xsl:when test="preceding::bibl[1]/editor = .">
            <xsl:text>----.&#160;</xsl:text>
          </xsl:when>
          <xsl:when test="preceding::bibl[1]/*/author = .">
            <xsl:text>----.&#160;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>----.&#160;</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        
        <xsl:choose>
          <xsl:when test="child::surname">
            <xsl:choose>
              <xsl:when test="following-sibling::author">
                <xsl:value-of select="surname"/>,
                <xsl:text>&#160;</xsl:text>
                <xsl:value-of select="forename"/>
                <xsl:text>,&#160;</xsl:text>
              </xsl:when>
              <xsl:when test="preceding-sibling::author">
                <xsl:text>and </xsl:text>
                <xsl:value-of select="forename"/>
                <xsl:text>&#160;</xsl:text>
                <xsl:value-of select="surname"/>
                <xsl:text>.&#160;</xsl:text>
              </xsl:when>
              <xsl:when test="substring($fname, string-length($fname)) = '.'">
                <xsl:value-of select="surname"/>, <xsl:value-of select="forename"
                /><xsl:text>&#160;</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="surname"/>, <xsl:value-of select="forename"
                /><xsl:text>.&#160;</xsl:text>
              </xsl:otherwise>
              
            </xsl:choose>
          </xsl:when>
          <xsl:when test="child::name">
            <xsl:apply-templates/>
            <xsl:text>.&#160;</xsl:text>
          </xsl:when>
          <xsl:when test="substring(., string-length(.)) = '.'">
            <xsl:apply-templates/>
            <xsl:text>&#160;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:apply-templates/>
            <xsl:text>.&#160;</xsl:text>            
          </xsl:otherwise>
        </xsl:choose>
        
      </xsl:otherwise>
        </xsl:choose>
  </xsl:template>
    <xsl:template match="editor">
    <xsl:choose>
      <xsl:when
        test="preceding::biblStruct[1]/*/editor = . or preceding::biblStruct[1]/*/author = .">
        <xsl:choose>
          <xsl:when test="@role='trans'">
            <xsl:text>----, trans.&#160;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:choose>
              <xsl:when test="following-sibling::editor">
                <xsl:text>---- and </xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:text>----, ed.&#160;</xsl:text>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:when test="@role='trans'">
        <xsl:choose>
          <xsl:when test="child::surname">
            <xsl:value-of select="surname"/>, <xsl:value-of select="forename"
            /><xsl:text>, trans.&#160;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:apply-templates/>
            <xsl:text>, trans.&#160;</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:when test="@role='ed'">
        <xsl:choose>
          <xsl:when test="child::surname">
            <xsl:value-of select="surname"/>, <xsl:value-of select="forename"
            /><xsl:text>, ed.&#160;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:choose>
              <xsl:when test="following-sibling::editor">
                <xsl:apply-templates/>
                <xsl:text> and </xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates/>
                <xsl:text>, ed.&#160;</xsl:text>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <xsl:choose>
          <xsl:when test="child::surname">
            <xsl:value-of select="surname"/>, <xsl:value-of select="forename"
            /><xsl:text>, ed.&#160;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:apply-templates/>
            <xsl:text>, ed.&#160;</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

 <xsl:template match="monogr[@rend]">
  <xsl:variable name="monogrnote" select="@rend"/>
  <xsl:value-of select="$monogrnote"/>
  <xsl:text> </xsl:text>
  <xsl:apply-templates/>
 </xsl:template>

 <xsl:template match="imprint[@rend]">
  <xsl:variable name="imprintnote" select="@rend"/> [<xsl:value-of select="$imprintnote"
  /><xsl:text>: </xsl:text><xsl:apply-templates/>] </xsl:template>

 <xsl:template match="edition">
  <xsl:apply-templates/>
  <xsl:text>. </xsl:text>
 </xsl:template>

 <xsl:template match="pubPlace"><xsl:apply-templates/>:&#160;</xsl:template>
 <xsl:template match="publisher">
<xsl:choose>
 <xsl:when test="ancestor::monogr[1]/title[@level='j']"><xsl:apply-templates/>&#160;
</xsl:when>
<xsl:otherwise>
<xsl:apply-templates/>,&#160;
</xsl:otherwise>
</xsl:choose>
 </xsl:template>

 <xsl:template match="biblScope">
  <xsl:choose>
   <xsl:when test="ancestor::listBibl">
    <xsl:choose>
     <xsl:when test="@type='vol'">
      <xsl:choose>
       <xsl:when test="ancestor::monogr[1]/title[@level='j']"
        ><xsl:apply-templates/>.&#160;</xsl:when>
       <xsl:otherwise>vol. <xsl:apply-templates/>, </xsl:otherwise>
      </xsl:choose>
     </xsl:when>
     <xsl:when test="@type='pp'">
      <xsl:choose>
       <xsl:when test="ancestor::monogr[1]/title[@level='j']"><xsl:apply-templates/>. </xsl:when>
       <xsl:when test="ancestor::monogr[1]/title[@level='m']"><xsl:apply-templates/>. </xsl:when>
       <xsl:otherwise>pp. <xsl:apply-templates/>. </xsl:otherwise>
      </xsl:choose>
     </xsl:when>
     <xsl:when test="@type='canonref'">
      <xsl:apply-templates/>. </xsl:when>
     <xsl:when test="@type='issue'"> (<xsl:apply-templates/>) </xsl:when>
     <xsl:otherwise>
      <xsl:apply-templates/>
      <xsl:text> </xsl:text>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:when>
   <xsl:when test="ancestor::cit | ancestor::p | ancestor::quote | ancestor::lg | ancestor::ptr">
    (<xsl:apply-templates/>) </xsl:when>
   <xsl:otherwise>
    <xsl:apply-templates/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

</xsl:stylesheet>
