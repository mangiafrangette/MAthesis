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
   
   <!-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
   <!-- dynaXML Stylesheet                                                     -->
   <!-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
   
   <!--
      Copyright (c) 2008, Regents of the University of California
      All rights reserved.
      
      Redistribution and use in source and binary forms, with or without 
      modification, are permitted provided that the following conditions are 
      met:
      
      - Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
      - Redistributions in binary form must reproduce the above copyright 
      notice, this list of conditions and the following disclaimer in the 
      documentation and/or other materials provided with the distribution.
      - Neither the name of the University of California nor the names of its
      contributors may be used to endorse or promote products derived from 
      this software without specific prior written permission.
      
      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
      AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
      IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
      ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
      LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
      CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
      SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
      INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
      CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
      ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
      POSSIBILITY OF SUCH DAMAGE.
   -->
   
   <!-- ====================================================================== -->
   <!-- Import Common Templates                                                -->
   <!-- ====================================================================== -->
   
   <xsl:import href="../common/docFormatterCommon.xsl"/>
   <xsl:import href="../../../crossQuery/resultFormatter/common/resultFormatterCommon.xsl"/>
   
   <!-- ====================================================================== -->
   <!-- Output Format                                                          -->
   <!-- ====================================================================== -->
   
   <xsl:output name="xhtml" method="xhtml" indent="no" 
      encoding="UTF-8" media-type="text/html; charset=UTF-8" 
      doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" 
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" 
      exclude-result-prefixes="#all"
      omit-xml-declaration="yes"/>
 
   <!-- ====================================================================== -->
   <!-- Strip Space                                                            -->
   <!-- ====================================================================== -->
   
   <xsl:strip-space elements="*"/>
   
   <!-- ====================================================================== -->
   <!-- Included Stylesheets                                                   -->
   <!-- ====================================================================== -->
   
   <xsl:include href="component.xsl"/>
   <xsl:include href="search.xsl"/>
   <xsl:include href="parameter.xsl"/>
   <xsl:include href="structure.xsl"/>
   <xsl:include href="table.xsl"/>
   <xsl:include href="titlepage.xsl"/>
   <xsl:include href="biblStruct.xsl"/>
   
   <!-- ====================================================================== -->
   <!-- Define Keys                                                            -->
   <!-- ====================================================================== -->
   
   <xsl:key name="pb-id" match="*[matches(name(),'^pb$|^milestone$')]" use="@*:id"/>
   <xsl:key name="ref-id" match="*[matches(name(),'^ref$')]" use="@*:id"/>
   <xsl:key name="fnote-id" match="*[matches(name(),'^note$')][@type='footnote' or @place='foot']" use="@*:id"/>
   <xsl:key name="endnote-id" match="*[matches(name(),'^note$')][@type='endnote' or @place='end']" use="@*:id"/>
   <xsl:key name="div-id" match="*[matches(name(),'^div')]" use="@*:id"/>
   <xsl:key name="generic-id" match="*[matches(name(),'^note$')][not(@type='footnote' or @place='foot' or @type='endnote' or @place='end')]|*[matches(name(),'^figure$|^bibl$|^table$')]" use="@*:id"/>
   

   <!-- ====================================================================== -->
   <!-- Root Template                                                          -->
   <!-- ====================================================================== -->
   
   <xsl:template match="/">
      <xsl:choose>
         <!-- robot solution -->
         <xsl:when test="matches($http.user-agent,$robots)">
            <xsl:call-template name="robot"/>
         </xsl:when>
         <xsl:when test="$doc.view='bbar'">
            <xsl:call-template name="bbar"/>
         </xsl:when>
         <xsl:when test="$doc.view='content'">
            <xsl:call-template name="content"/>
         </xsl:when>
         <xsl:when test="$doc.view='popup'">
            <xsl:call-template name="popup"/>
         </xsl:when>
         <xsl:when test="$doc.view='citation'">
            <xsl:call-template name="citation"/>
         </xsl:when>
         <xsl:when test="$doc.view='print'">
            <xsl:call-template name="print"/>
         </xsl:when>
         <xsl:when test="$doc.view='xml'">
            <xsl:call-template name="xml"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:call-template name="frames"/>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- TEI-specific parameters                                                -->
   <!-- ====================================================================== -->
   
   <!-- If a query was specified but no particular hit rank, jump to the first hit 
        (in document order) 
   -->
   <xsl:param name="hit.rank">
      <xsl:choose>
         <xsl:when test="$query and not($query = '0')">
         </xsl:when>
         <xsl:otherwise>
            <xsl:value-of select="'0'"/>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:param>
   
   <!-- To support direct links from snippets, the following two parameters must check value of $hit.rank -->
   <xsl:param name="chunk.id">
      <xsl:choose>
         <xsl:when test="$hit.rank != '0' and key('hit-rank-dynamic', $hit.rank)/ancestor::*[matches(name(),'^div')]">
            <xsl:value-of select="key('hit-rank-dynamic', $hit.rank)/ancestor::*[matches(local-name(),'^div')][1]/@*:id"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:value-of select="'0'"/>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:param>
   
   <xsl:param name="toc.id">
      <xsl:choose>
         <xsl:when test="$hit.rank != '0' and key('hit-rank-dynamic', $hit.rank)/ancestor::*[matches(name(),'^div')]">
            <xsl:value-of select="key('hit-rank-dynamic', $hit.rank)/ancestor::*[matches(local-name(),'^div')][1]/parent::*/@*:id"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:value-of select="'0'"/>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:param>
   
   <!-- ====================================================================== -->
   <!--   Using selector language from resultFormatter                               -->
   <!-- ====================================================================== -->
   
   <xsl:template name="topLevel">
   <xsl:for-each select="tei:TEI/tei:teiHeader/tei:fileDesc">
      <strong><xsl:text>Title: </xsl:text></strong><xsl:text>"</xsl:text>
         <xsl:value-of select="tei:titleStmt/tei:title[@type='main']"/><xsl:text>"</xsl:text>
   </xsl:for-each> <br/>
     <xsl:for-each select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt">
        <strong><xsl:text>Author: </xsl:text></strong>
            <xsl:value-of select="tei:author[1]/tei:name/tei:forename[@type='first']"/>
            <xsl:text> </xsl:text>
        <xsl:value-of select="tei:author[1]/tei:name/tei:surname"/>
   </xsl:for-each><br/>
      <xsl:for-each select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt">
         <strong><xsl:text>Affiliation: </xsl:text></strong>
         <xsl:value-of select="tei:author[1]/tei:name/tei:affiliation"/>
      </xsl:for-each><br/>
      <xsl:for-each select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt">
         <strong><xsl:text>Conference location: </xsl:text></strong>
         <xsl:value-of select="tei:publisher/tei:name"/>
      </xsl:for-each><br/>
      <xsl:for-each select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt">
         <strong> <xsl:text>Date: </xsl:text></strong>
         <xsl:value-of select="tei:date"/>
      </xsl:for-each><br/>
</xsl:template>

   <!-- ====================================================================== -->
   <!-- Content Template                                                       -->
   <!-- ====================================================================== -->
   <xsl:template name="content">
      <xsl:for-each select="tei:TEI">
         <h3><xsl:text>Abstract</xsl:text></h3>
         <xsl:value-of select="tei:text"/>
      </xsl:for-each>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- Lists                                                                  -->
   <!-- ====================================================================== -->
   
  <!-- <xsl:template match="*:list">
      <xsl:choose>
         <xsl:when test="@type='gloss'">
            <dl><xsl:apply-templates/></dl>
         </xsl:when>
         <xsl:when test="@type='simple'">
            <ul class="nobull"><xsl:apply-templates/></ul>
         </xsl:when>
         <xsl:when test="@type='ordered'">
            <xsl:choose>
               <xsl:when test="@rend='alpha'">
                  <ol class="alpha"><xsl:apply-templates/></ol>
               </xsl:when>
               <xsl:otherwise>
                  <ol><xsl:apply-templates/></ol>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:when>
         <xsl:when test="@type='unordered'">
            <ul><xsl:apply-templates/></ul>
         </xsl:when>
         <xsl:when test="@type='bulleted'">
            <xsl:choose>
               <xsl:when test="@rend='dash'">
                  <ul class="nobull"><xsl:text>- </xsl:text><xsl:apply-templates/></ul>
               </xsl:when>
               <xsl:otherwise>
                  <ul><xsl:apply-templates/></ul>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:when>
         <xsl:when test="@type='bibliographic'">
            <ol><xsl:apply-templates/></ol>
         </xsl:when>
         <xsl:when test="@type='special'">
            <ul><xsl:apply-templates/></ul>
         </xsl:when>
      </xsl:choose>
   </xsl:template> -->
   
   <!-- ADHO list/item special case -->
   <xsl:template match="*:list/*:item/*:list/*:item">
            <ul><xsl:apply-templates/></ul>
   </xsl:template>
 
   
  <xsl:template match="*:list">
      <xsl:choose>
         <xsl:when test="*:item">
            <item><xsl:apply-templates/></item>
            <xsl:text>&#x0A;</xsl:text>
         </xsl:when>
         <xsl:otherwise>
            <ul><xsl:apply-templates/></ul>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template> 
   
   <xsl:template  match="*:label">
      <dt><xsl:apply-templates/></dt>
   </xsl:template>
   
   <xsl:template match="*:name">
      <xsl:apply-templates/>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- Heads                                                                  -->
   <!-- ====================================================================== -->
   
   <xsl:template match="*:head">
      
      <xsl:variable name="type" select="parent::*/@type"/>
      
      <xsl:variable name="class">
         <xsl:choose>
            <xsl:when test="@rend">
               <xsl:value-of select="@rend"/>
            </xsl:when>
            <xsl:otherwise>normal</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      
      <xsl:choose>
         <xsl:when test="@type='sub' or @type='subtitle'">
            <!-- Needs more choices here -->
            <h3 class="{$class}"><xsl:apply-templates/></h3>
         </xsl:when>
         <xsl:when test="$type='fmsec'">
            <h2 class="{$class}"><xsl:apply-templates/></h2>
         </xsl:when>
         <xsl:when test="$type='volume'">
            <h1 class="{$class}">
               <xsl:if test="parent::*/@n">
                  <xsl:value-of select="parent::*/@n"/><xsl:text>. </xsl:text>
               </xsl:if>
               <xsl:apply-templates/>
            </h1>
         </xsl:when>
         <xsl:when test="$type='part'">
            <h1 class="{$class}">
               <xsl:if test="parent::*/@n">
                  <xsl:value-of select="parent::*/@n"/><xsl:text>. </xsl:text>
               </xsl:if>
               <xsl:apply-templates/>
            </h1>
         </xsl:when>
         <xsl:when test="$type='chapter'">
            <h2 class="{$class}">
               <xsl:if test="parent::*/@n">
                  <xsl:value-of select="parent::*/@n"/><xsl:text>. </xsl:text>
               </xsl:if>
               <xsl:apply-templates/>
            </h2>
         </xsl:when>
         <xsl:when test="$type='ss1'">
            <h3 class="{$class}">
               <xsl:if test="parent::*/@n">
                  <xsl:value-of select="parent::*/@n"/><xsl:text>. </xsl:text>
               </xsl:if>
               <xsl:apply-templates/>
            </h3>
         </xsl:when>
         <xsl:when test="$type='ss2'">
            <h3 class="{$class}"><xsl:apply-templates/></h3>
         </xsl:when>
         <xsl:when test="$type='ss3'">
            <h3 class="{$class}"><xsl:apply-templates/></h3>
         </xsl:when>
         <xsl:when test="$type='ss4'">
            <h4 class="{$class}"><xsl:apply-templates/></h4>
         </xsl:when>
         <xsl:when test="$type='ss5'">
            <h4 class="{$class}"><xsl:apply-templates/></h4>
         </xsl:when>
         <xsl:when test="$type='bmsec'">
            <h2 class="{$class}"><xsl:apply-templates/></h2>
         </xsl:when>
         <xsl:when test="$type='appendix'">
            <h2 class="{$class}">
               <xsl:if test="parent::*/@n">
                  <xsl:value-of select="parent::*/@n"/><xsl:text>. </xsl:text>
               </xsl:if>
               <xsl:apply-templates/>
            </h2>
         </xsl:when>
         <xsl:when test="$type='endnotes'">
            <h3 class="{$class}"><xsl:apply-templates/></h3>
         </xsl:when>
         <xsl:when test="$type='bibliography'">
            <h2 class="{$class}"><xsl:apply-templates/></h2>
         </xsl:when>
         <xsl:when test="$type='glossary'">
            <h2 class="{$class}"><xsl:apply-templates/></h2>
         </xsl:when>
         <xsl:when test="$type='index'">
            <h2 class="{$class}"><xsl:apply-templates/></h2>
         </xsl:when>
         <xsl:otherwise>
            <h4 class="{$class}"><xsl:apply-templates/></h4>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>
   
   <xsl:template match="*:docAuthor">
      <h4><xsl:apply-templates/></h4>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- Notes                                                                  -->
   <!-- ====================================================================== -->
   
   <xsl:template match="*:note">
      <xsl:choose>
         <xsl:when test="@type='footnote' or @place='foot'">
            <xsl:if test="$doc.view='popup' or $doc.view='print'">
               <xsl:apply-templates/>
            </xsl:if>
         </xsl:when>
         <xsl:when test="@type='endnote' or @place='end'">
            <xsl:choose>
               <xsl:when test="$anchor.id=@*:id">
                  <a name="X"></a>
                  <div class="note-hi">
                     <xsl:apply-templates/>
                  </div>
               </xsl:when>
               <xsl:otherwise>
                  <div class="note">
                     <xsl:apply-templates/>
                  </div>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:when>
         <xsl:when test="@type='note' or @place='inline'">
            <div class="inline-note">
               <xsl:apply-templates/>
            </div>
         </xsl:when>
         <xsl:otherwise>
            <div class="note">
               <xsl:apply-templates/>
            </div>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>
   
   <xsl:template match="*:p[ancestor::note[@type='footnote' or @place='foot']]">
      
      <xsl:variable name="n" select="parent::note/@n"/>
      
      <p>
         <xsl:if test="position()=1">
            <xsl:if test="$n != ''">
               <xsl:text>[</xsl:text><xsl:value-of select="$n"/><xsl:text>] </xsl:text>
            </xsl:if>
         </xsl:if>
         <xsl:apply-templates/>
      </p>
      
   </xsl:template>
   
   <xsl:template match="*:p[ancestor::note[@type='endnote' or @place='end']]">
      
      <xsl:variable name="n" select="parent::note/@n"/>
      
      <xsl:variable name="class">
         <xsl:choose>
            <xsl:when test="position()=1">noindent</xsl:when>
            <xsl:otherwise>indent</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      
      <p class="{$class}">
         <xsl:if test="position()=1">
            <xsl:if test="$n != ''">
               <xsl:value-of select="$n"/><xsl:text>. </xsl:text>
            </xsl:if>
         </xsl:if>
         <xsl:apply-templates/>
         <xsl:if test="position()=last()">
            <xsl:if test="parent::note/@corresp">
               
               <xsl:variable name="corresp" select="parent::note/@corresp"/>
               
               <xsl:variable name="chunk" select="key('ref-id', $corresp)/ancestor::*[matches(local-name(), '^div[1-6]$')][1]/@*:id"/>
               
               <xsl:variable name="toc" select="key('div-id', $chunk)/parent::*/@*:id"/>
               
               <span class="down1">
                  <xsl:text> [</xsl:text>
                  <a>
                     <xsl:attribute name="href"><xsl:value-of select="$doc.path"/>&#038;chunk.id=<xsl:value-of select="$chunk"/>&#038;toc.id=<xsl:value-of select="$toc"/>&#038;toc.depth=<xsl:value-of select="$toc.depth"/>&#038;brand=<xsl:value-of select="$brand"/><xsl:value-of select="$search"/>&#038;anchor.id=<xsl:value-of select="$corresp"/>#X</xsl:attribute>
                     <xsl:attribute name="target">_top</xsl:attribute>
                     <xsl:text>BACK</xsl:text>
                  </a>
                  <xsl:text>]</xsl:text>
               </span>
            </xsl:if>
         </xsl:if>
      </p>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- Single-view (was Frames) Template -->
   <!-- ====================================================================== -->
   
   <xsl:template name="frames" exclude-result-prefixes="#all">   
      <xsl:variable name="bbar.href"><xsl:value-of select="$query.string"/>&#038;doc.view=bbar&#038;chunk.id=<xsl:value-of select="$chunk.id"/>&#038;brand=<xsl:value-of select="$brand"/><xsl:value-of select="$search"/></xsl:variable> 
      <xsl:variable name="xml.href"><xsl:value-of select="$query.string"/>&#038;doc.view=xml&#038;chunk.id=<xsl:value-of select="$chunk.id"/>&#038;brand=<xsl:value-of select="$brand"/><xsl:value-of select="$search"/></xsl:variable> 
      <xsl:variable name="toc.href"><xsl:value-of select="$query.string"/>&#038;doc.view=toc&#038;chunk.id=<xsl:value-of select="$chunk.id"/>&#038;brand=<xsl:value-of select="$brand"/>&#038;<xsl:value-of select="$search"/>#X</xsl:variable>
      <xsl:variable name="content.href"><xsl:value-of select="$query.string"/>&#038;doc.view=content&#038;chunk.id=<xsl:value-of select="$chunk.id"/>&#038;brand=<xsl:value-of select="$brand"/><xsl:value-of select="$search"/></xsl:variable>
      
      <html xml:lang="en" lang="en">
         <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <title>
               <xsl:value-of select="$doc.title"/>
            </title>
            <xsl:copy-of select="$brand.links"/>
            <link rel="shortcut icon" href="icons/brand/favicon.ico" />
            <link rel="stylesheet" type="text/css" href="css/brand/tei.css"/>
            <link rel="stylesheet" type="text/css" href="css/brand/results.css"/>
            <!-- AJAX support -->
            <script src="{$xtfURL}script/connection-min.js" type="text/javascript"/> 
            <script src="{$xtfURL}script/jquery.js" type="text/javascript"/> 
            <script src="{$xtfURL}script/jquery-ui.js" type="text/javascript"/> 
            <script src="{$xtfURL}script/bookbag.js" type="text/javascript"/>
            <script src="{$xtfURL}script/moreLike.js" type="text/javascript"/>
         </head>
         <body>         
               <div class="bbar">
                  <xsl:attribute name="name">bbar</xsl:attribute>
                  <xsl:attribute name="src"><xsl:value-of select="$xtfURL"/>view?<xsl:value-of select="$bbar.href"/></xsl:attribute> 
                  <xsl:call-template name="bbar"/>
               </div> 
                <div class="topLevel">
                 <xsl:call-template name="topLevel"/>      
                </div>
            <div class="content">
               <xsl:attribute name="name">content</xsl:attribute>
             <xsl:attribute name="src"><xsl:value-of select="$xtfURL"/>view?<xsl:value-of select="$content.href"/></xsl:attribute> 
               <h2><xsl:text>Abstract</xsl:text></h2>
               <xsl:apply-templates select="/*/*:text/*"/>
            </div>
            
            <div>
            <xsl:copy-of select="$brand.footer"/>
            </div>
            </body>
         </html>
   </xsl:template>
   

   
   <!-- ====================================================================== -->
   <!-- Print Template                                                  -->
   <!-- ====================================================================== -->
   
   <xsl:template name="print" exclude-result-prefixes="#all">
      <html xml:lang="en" lang="en">
         <head>
            <title>
               <xsl:value-of select="$doc.title"/>
            </title>
            <link rel="stylesheet" type="text/css" href="css/brand/print.css"/>
         </head>
            <div align="center">
               <table width="80%">
                        <tr>
                           <td>
                              <xsl:choose>
                                 <xsl:when test="$chunk.id != '0'">
                                    <xsl:apply-templates select="key('div-id', $chunk.id)"/>
                                 </xsl:when>
                                 <xsl:otherwise>
                                    <div class="topLevel">
                                       <xsl:call-template name="topLevel"/>      
                                    </div>
                                    <xsl:apply-templates select="/*/*:text/*"/>
                                 </xsl:otherwise>
                              </xsl:choose>
                           </td>
                        </tr>
               </table>
            </div>
      </html>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- Anchor Template                                                        -->
   <!-- ====================================================================== -->
   
   <xsl:template name="create.anchor">
      <xsl:choose>
         <!-- First so it takes precedence over computed hit.rank -->
         <xsl:when test="($query != '0' and $query != '') and $set.anchor != '0'">
            <xsl:text>#</xsl:text><xsl:value-of select="$set.anchor"/>
         </xsl:when>
         <!-- Next is hit.rank -->
         <xsl:when test="($query != '0' and $query != '') and $hit.rank != '0'">
            <xsl:text>#</xsl:text><xsl:value-of select="key('hit-rank-dynamic', $hit.rank)/@hitNum"/>
         </xsl:when>
         <xsl:when test="($query != '0' and $query != '') and $chunk.id != '0'">
            <xsl:text>#</xsl:text><xsl:value-of select="key('div-id', $chunk.id)/@xtf:firstHit"/>
         </xsl:when>
         <xsl:when test="$anchor.id != '0'">
            <xsl:text>#X</xsl:text>
         </xsl:when>
      </xsl:choose>
   </xsl:template>
   
   <!-- ====================================================================== -->
   <!-- Popup Window Template                                                  -->
   <!-- ====================================================================== -->
  
   <xsl:template name="popup" exclude-result-prefixes="#all">
      <html xml:lang="en" lang="en">
         <head>
            <title>
               <xsl:choose>
                  <xsl:when test="(key('fnote-id', $chunk.id)/@type = 'footnote') or (key('fnote-id', $chunk.id)/@place = 'foot')">
                     <xsl:text>Footnote</xsl:text>
                  </xsl:when>
                  <xsl:when test="key('div-id', $chunk.id)/@type = 'dedication'">
                     <xsl:text>Dedication</xsl:text>
                  </xsl:when>
                  <xsl:when test="key('div-id', $chunk.id)/@type = 'copyright'">
                     <xsl:text>Copyright</xsl:text>
                  </xsl:when>
                  <xsl:when test="key('div-id', $chunk.id)/@type = 'epigraph'">
                     <xsl:text>Epigraph</xsl:text>
                  </xsl:when>
                  <xsl:when test="$fig.ent != '0'">
                     <xsl:text>Illustration</xsl:text>
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:text>popup</xsl:text>
                  </xsl:otherwise>
               </xsl:choose>
            </title>
            <link rel="stylesheet" type="text/css" href="css/brand/content.css"/>
            <link rel="shortcut icon" href="icons/brand/favicon.ico" />
 
         </head>
         <body>
            <div class="content">
               <xsl:choose>
                  <xsl:when test="(key('fnote-id', $chunk.id)/@type = 'footnote') or (key('fnote-id', $chunk.id)/@place = 'foot')">
                     <xsl:apply-templates select="key('fnote-id', $chunk.id)"/>  
                  </xsl:when>
                  <xsl:when test="key('div-id', $chunk.id)/@type = 'dedication'">
                     <xsl:apply-templates select="key('div-id', $chunk.id)" mode="titlepage"/>  
                  </xsl:when>
                  <xsl:when test="key('div-id', $chunk.id)/@type = 'copyright'">
                     <xsl:apply-templates select="key('div-id', $chunk.id)" mode="titlepage"/>  
                  </xsl:when>
                  <xsl:when test="key('div-id', $chunk.id)/@type = 'epigraph'">
                     <xsl:apply-templates select="key('div-id', $chunk.id)" mode="titlepage"/>  
                  </xsl:when>
                  <xsl:when test="$fig.ent != '0'">
                     <img src="{$fig.ent}" alt="full-size image"/>        
                  </xsl:when>
               </xsl:choose>
               <p>
                  <a>
                     <xsl:attribute name="href">javascript://</xsl:attribute>
                     <xsl:attribute name="onclick">
                        <xsl:text>javascript:window.close('popup')</xsl:text>
                     </xsl:attribute>
                     <span class="down1">Close this Window</span>
                  </a>
               </p>
            </div>
         </body>
      </html>
   </xsl:template> 
   
</xsl:stylesheet>  