<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
   xmlns:ns="http://www.tei-c.org/ns/1.0" 
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:date="http://exslt.org/dates-and-times"
   xmlns:parse="http://cdlib.org/xtf/parse"
   xmlns:xtf="http://cdlib.org/xtf"
   xmlns:session="java:org.cdlib.xtf.xslt.Session"
   xmlns:editURL="http://cdlib.org/xtf/editURL"
   xmlns:FileUtils="java:org.cdlib.xtf.xslt.FileUtils"
   extension-element-prefixes="date FileUtils"
   exclude-result-prefixes="#all">
   
   
   
   <!-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
   <!-- Search forms stylesheet                                                -->
   
   <!-- DH-abstracts: remove Freeform                                          -->
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
   <!-- Global parameters                                                      -->
   <!-- ====================================================================== -->
   
  <!-- <xsl:param name="freeformQuery"/> -->
   
   <!-- ====================================================================== -->
   <!-- Form Templates                                                         -->
   <!-- ====================================================================== -->
   
   <!-- main form page -->
   <xsl:template match="crossQueryResult" mode="form" exclude-result-prefixes="#all">
      <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
         <head>
            <title>DH Abstracts: Search Form</title>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <xsl:copy-of select="$brand.links"/>
         </head>
         <body>
            <xsl:copy-of select="$brand.header"/>
            <div class="searchPage">
               <div class="forms">
                  <table>
                     <tr>
                        <td class="{if(matches($smode,'simple')) then 'tab-select' else 'tab'}"><a href="search?smode=simple">Keyword</a></td>
                        <td class="{if(matches($smode,'advanced')) then 'tab-select' else 'tab'}"><a href="search?smode=advanced">Advanced</a></td>
                    <!--    <td class="{if(matches($smode,'freeform')) then 'tab-select' else 'tab'}"><a href="search?smode=freeform">Freeform</a></td> -->
                        <td class="{if(matches($smode,'browse')) then 'tab-select' else 'tab'}"><a href="search?smode=browse">Browse</a></td>
                     </tr>
                     <tr>
                        <td colspan="3"> <!-- reduced to 3 from 4 for absent Freeform -->
                           <div class="form">
                              <xsl:choose>
                                 <xsl:when test="matches($smode,'simple')">
                                    <xsl:call-template name="simpleForm"/>
                                 </xsl:when>
                                 <xsl:when test="matches($smode,'advanced')">
                                    <xsl:call-template name="advancedForm"/>
                                 </xsl:when>
                              <!--   <xsl:when test="matches($smode,'freeform')">
                                    <xsl:call-template name="freeformForm"/>
                                 </xsl:when>  -->
                                 <xsl:when test="matches($smode,'browse')">
                                    <table>
                                       <tr>
                                          <td>
                                             <p>Browse all documents by the available facets, or alphanumerically by author or title:</p>
                                          </td>
                                       </tr>
                                       <tr>
                                          <td>
                                             <xsl:call-template name="browseLinks"/>
                                          </td>
                                       </tr>
                                    </table>
                                 </xsl:when>
                              </xsl:choose>
                           </div>
                        </td>
                     </tr>
                  </table>
               </div>
            </div>
            <xsl:copy-of select="$brand.footer"/>
         </body>
      </html>
   </xsl:template>
   
   <!-- simple form -->
   <xsl:template name="simpleForm" exclude-result-prefixes="#all">
      <form method="get" action="{$xtfURL}{$crossqueryPath}">
         <table>
            <tr>
               <td>  
            <!-- isolated search box and button within form tag to resize search box -->      
                    <input type="text" name="keyword" value="{$keyword}" placeholder=" Search..."></input>
                     <xsl:text>&#160;</xsl:text>
                  <input type="submit" value="Enter"/>
                  <input type="reset" onclick="location.href='{$xtfURL}{$crossqueryPath}'" value="Clear"/>
               </td>
            </tr>
         </table>   
      </form>
      <!-- bracketed search box and sampleTable into separate forms -->
           <form>
              <table class="sampleTable">
                     <tr>
                        <td colspan="2"><b>Examples:</b></td>                  
                     </tr>
                     <tr>
                        <td class="sampleQuery">rhetoric</td>
                        <td class="sampleDescrip">Search keywords (full text and metadata) for 'rhetoric'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">digital archive</td>
                        <td class="sampleDescrip">Search keywords for 'digital' AND 'archive'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">"text analysis"</td>
                        <td class="sampleDescrip">Search keywords for the phrase 'text analysis'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">tech*</td>
                        <td class="sampleDescrip">Search keywords for the string 'tech' followed by 0 or more characters</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">epigraph?</td>
                        <td class="sampleDescrip">Search keywords for the string 'epigraph' followed by a single character</td>
                     </tr>
         </table>
      </form>
   </xsl:template>
   
   <!-- advanced form -->
   <xsl:template name="advancedForm" exclude-result-prefixes="#all">
      <form method="get" action="{$xtfURL}{$crossqueryPath}">
   <div class="center-buttons">
            <input type="hidden" name="smode" value="advanced"/>
            <input type="submit" value="Search"/>
            <input type="reset" onclick="location.href='{$xtfURL}{$crossqueryPath}?smode=advanced'" value="Clear"/>
   </div>
      <p class="clear"></p>
         
         <table class="top_table">
            <tr>
               <td>
                  <table class="left_table">
                     <tr>
                        <td colspan="3">
                           <h4>Search Entire Text</h4>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td colspan="2">
                           <input type="text" name="text" size="30" value="{$text}" placeholder=" Search all"/>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td colspan="2">
                           <xsl:choose>
                              <xsl:when test="$text-join = 'or'">
                                 <input type="radio" name="text-join" value=""/>
                                 <xsl:text> all of </xsl:text>
                                 <input type="radio" name="text-join" value="or" checked="checked"/>
                                 <xsl:text> any of </xsl:text>
                              </xsl:when>
                              <xsl:otherwise>
                                 <input type="radio" name="text-join" value="" checked="checked"/>
                                 <xsl:text> all of </xsl:text>
                                 <input type="radio" name="text-join" value="or"/>
                                 <xsl:text> any of </xsl:text>
                              </xsl:otherwise>
                           </xsl:choose>
                           <xsl:text>these words</xsl:text>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Exclude</td>
                        <td>
                           <input type="text" name="text-exclude" size="20" value="{$text-exclude}" placeholder=" Exclude"/>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Proximity</td>
                        <td>
                           <select size="1" name="text-prox">
                              <xsl:choose>
                                 <xsl:when test="$text-prox = '1'">
                                    <option value=""></option>
                                    <option value="1" selected="selected">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                 </xsl:when>
                                 <xsl:when test="$text-prox = '2'">
                                    <option value=""></option>
                                    <option value="1">1</option>
                                    <option value="2" selected="selected">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                 </xsl:when>
                                 <xsl:when test="$text-prox = '3'">
                                    <option value=""></option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3" selected="selected">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                 </xsl:when>
                                 <xsl:when test="$text-prox = '4'">
                                    <option value=""></option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4" selected="selected">4</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                 </xsl:when>
                                 <xsl:when test="$text-prox = '5'">
                                    <option value=""></option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5" selected="selected">5</option>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                 </xsl:when>
                                 <xsl:when test="$text-prox = '10'">
                                    <option value=""></option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="10" selected="selected">10</option>
                                    <option value="20">20</option>
                                 </xsl:when>
                                 <xsl:when test="$text-prox = '20'">
                                    <option value=""></option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="20" selected="selected">20</option>
                                 </xsl:when>
                                 <xsl:otherwise>
                                    <option value="" selected="selected"></option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                 </xsl:otherwise>
                              </xsl:choose>
                           </select>
                           <xsl:text> word(s)</xsl:text>
                        </td>
                     </tr>           
                <tr>
                        <td class="indent">&#160;</td>
                        <td>Section</td>
                        <td> <br/>
                           <xsl:choose>
                         
                              <xsl:when test="$sectionType = 'head'">
                                 <input type="radio" name="sectionType" value=""/><xsl:text> any </xsl:text><br/>
                                 <input type="radio" name="sectionType" value="head" checked="checked"/><xsl:text> headings </xsl:text><br/>
                                 <input type="radio" name="sectionType" value="citation"/><xsl:text> citations </xsl:text>
                              </xsl:when>
                              <xsl:when test="$sectionType = 'note'"> 
                                 <input type="radio" name="sectionType" value=""/><xsl:text> any </xsl:text><br/>
                                 <input type="radio" name="sectionType" value="head"/><xsl:text> headings </xsl:text><br/>
                                 <input type="radio" name="sectionType" value="citation" checked="checked"/><xsl:text> citations </xsl:text>
                              </xsl:when>
                              <xsl:otherwise>
                                 <input type="radio" name="sectionType" value="" checked="checked"/><xsl:text> any </xsl:text><br/>
                                 <input type="radio" name="sectionType" value="head"/><xsl:text> headings </xsl:text><br/>
                                 <input type="radio" name="sectionType" value="citation"/><xsl:text> citations </xsl:text>
                              </xsl:otherwise>
                           </xsl:choose>
                        </td>
                     </tr>
                  </table>
               </td>
               <td>
                  <table class="right_table">
                     <tr>
                        <td colspan="3"><h4>Search Metadata</h4></td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Title</td>
                        <td>
                           <input type="text" name="title" size="20" value="{$title}" placeholder=" Title"/>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Author</td>
                        <td>
                           <input type="text" name="creator" size="20" value="{$creator}" placeholder=" Author"/>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Location</td>
                        <td>
                           <input type="text" name="location" size="20" value="{$location}" placeholder=" Location"/>
                        </td>
                     </tr>
                     <!-- ADHO disable subject display -->
                 <!--    <tr>
                        <td class="indent">&#160;</td>
                        <td><b>Subject</b></td>
                        <td>
                           <input type="text" name="subject" size="20" value="{$subject}" placeholder=" Subject"/>
                        </td>
                     </tr> -->
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Year(s)</td>
                        <td>
                           <xsl:text>From </xsl:text>
                           <input type="text" name="year" size="7" value="{$year}" placeholder=" begin"/>
                           <xsl:text> to </xsl:text>
                           <input type="text" name="year-max" size="7" value="{$year-max}" placeholder=" end"/>
                        </td>
                     </tr>
                     <tr>
                        <td class="indent">&#160;</td>
                        <td>Type</td>
                        <td>
                           <select size="1" name="type">
                              <option value="">All</option>
                              <option value="ead">EAD</option>
                              <option value="html">HTML</option>
                              <option value="word">Word</option>
                              <option value="nlm">NLM</option>
                              <option value="pdf">PDF</option>
                              <option value="tei">TEI</option>
                              <option value="text">Text</option>
                           </select>
                        </td>
                     </tr>
                  </table>
               </td>
            </tr>

          <!-- Omit sampleTable -->
           <!-- <tr>
               <td colspan="2">
                  <table class="sampleTable">
                     <tr>
                        <td colspan="3"><b>Examples:</b></td>                  
                     </tr>
                     <tr>
                        <td/>
                        <td class="sampleQuery">digital archive</td>
                        <td class="sampleDescrip">Search full text for 'digital' AND 'archive'</td>
                     </tr>
                     <tr>
                        <td>Exclude</td>
                        <td class="sampleQuery">SGML</td>
                        <td class="sampleDescrip">Exclude results which contain the term 'race'</td>
                     </tr>
                     <tr>
                        <td>Proximity</td>
                        <td><form action=""><select><option>5</option></select></form></td>
                        <td class="sampleDescrip">Match the full text terms, only if they are 5 or fewer words apart</td>
                     </tr>
                     <tr>
                        <td>Section</td>
                        <td><form action=""><input type="radio" checked="checked"/>headings</form></td>
                        <td class="sampleDescrip">Match the full text terms, only if they appear in document 'headings' (e.g. section titles)</td>
                     </tr>
                     <tr>
                        <td>Title</td>
                        <td class="sampleQuery">"text analysis"</td>
                        <td class="sampleDescrip">Search for the phrase 'south africa' in the 'title' field</td>
                     </tr>
                     <tr>
                        <td>Year(s)</td>
                        <td><form action="">from <input type="text" value="2000" size="4"/> to <input type="text" value="2005" size="4"/></form></td>
                        <td class="sampleDescrip">Search for documents whose date falls in the range from '2000' to '2005'</td>
                     </tr>
                  </table>
               </td>
            </tr> -->
         </table>
      </form>
   </xsl:template>
   
   <!-- free-form form 
   <xsl:template name="freeformForm" exclude-result-prefixes="#all">
      <form method="get" action="{$xtfURL}{$crossqueryPath}">
         <table>
            <tr>
               <td>
                  <p><i>Experimental feature:</i> "Freeform" complex query supporting -/NOT, |/OR, &amp;/AND, field names, and parentheses.</p>
                  <input type="text" name="freeformQuery" size="40" value="{$freeformQuery}"/>
                  <xsl:text>&#160;</xsl:text>
                  <input type="submit" value="Search"/>
                  <input type="reset" onclick="location.href='{$xtfURL}{$crossqueryPath}'" value="Clear"/>
               </td>
            </tr> 
            <tr>
               <td>
                  <table class="sampleTable">
                     <tr>
                        <td colspan="2"><b>Examples:</b></td>                  
                     </tr>
                     <tr>
                        <td class="sampleQuery">rhetoric</td>
                        <td class="sampleDescrip">Search keywords (full text and metadata) for 'africa'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south africa</td>
                        <td class="sampleDescrip">Search keywords for 'south' AND 'africa'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south &amp; africa</td>
                        <td class="sampleDescrip">(same)</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south AND africa</td>
                        <td class="sampleDescrip">(same; note 'AND' must be capitalized)</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">title:south africa</td>
                        <td class="sampleDescrip">Search title for 'south' AND 'africa'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">creator:moodley title:africa</td>
                        <td class="sampleDescrip">Search creator for 'moodley' AND title for 'africa'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south | africa</td>
                        <td class="sampleDescrip">Search keywords for 'south' OR 'africa'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south OR africa</td>
                        <td class="sampleDescrip">(same; note 'OR' must be capitalized)</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">africa -south</td>
                        <td class="sampleDescrip">Search keywords for 'africa' not near 'south'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">africa NOT south</td>
                        <td class="sampleDescrip">(same; note 'NOT' must be capitalized)</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">title:africa -south</td>
                        <td class="sampleDescrip">Search title for 'africa' not near 'south'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">title:africa subject:-politics</td>
                        <td class="sampleDescrip">
                           Search items with 'africa' in title but not 'politics' in subject.
                           Note '-' must follow ':'
                        </td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">title:-south</td>
                        <td class="sampleDescrip">Match all items without 'south' in title</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">-africa</td>
                        <td class="sampleDescrip">Match all items without 'africa' in keywords</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south (africa OR america)</td>
                        <td class="sampleDescrip">Search keywords for 'south' AND either 'africa' OR 'america'</td>
                     </tr>
                     <tr>
                        <td class="sampleQuery">south africa OR america</td>
                        <td class="sampleDescrip">(same, due to precedence)</td>
                     </tr>
                  </table>
               </td>
            </tr>
         </table>
      </form>
   </xsl:template> -->
   
</xsl:stylesheet>
