<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"
  exclude-result-prefixes="sm">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Sitemap — John Ngor Deng Garang</title>
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&amp;display=swap" rel="stylesheet"/>
        <style>
          *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

          body {
            font-family: 'Inter', sans-serif;
            background: #f8f9fa;
            color: #1a1a1a;
            min-height: 100vh;
          }

          /* ── Header ── */
          .sm-header {
            background: linear-gradient(135deg, #16b2dc 0%, #1a1a1a 100%);
            padding: 48px 0 40px;
            text-align: center;
          }
          .sm-header img {
            height: 48px;
            margin-bottom: 16px;
            display: block;
            margin-left: auto;
            margin-right: auto;
          }
          .sm-header h1 {
            font-size: 1.75rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: -0.02em;
          }
          .sm-header p {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.7);
            margin-top: 6px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
          }

          /* ── Container ── */
          .sm-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px 80px;
          }

          /* ── Stats bar ── */
          .sm-stats {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
          }
          .sm-stat {
            background: white;
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 0;
            padding: 14px 22px;
            flex: 1;
            min-width: 140px;
            text-align: center;
          }
          .sm-stat-num {
            font-size: 1.6rem;
            font-weight: 700;
            color: #16b2dc;
            line-height: 1;
          }
          .sm-stat-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888;
            margin-top: 4px;
          }

          /* ── Section label ── */
          .sm-section-label {
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #16b2dc;
            margin: 2rem 0 0.6rem;
            padding-left: 2px;
          }

          /* ── URL rows ── */
          .sm-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border: 1px solid rgba(0,0,0,0.08);
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
          }
          .sm-table thead tr {
            background: #1a1a1a;
          }
          .sm-table thead th {
            padding: 10px 16px;
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: rgba(255,255,255,0.7);
            text-align: left;
          }
          .sm-table tbody tr {
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.15s;
          }
          .sm-table tbody tr:last-child { border-bottom: none; }
          .sm-table tbody tr:hover { background: #f0fbff; }
          .sm-table td {
            padding: 12px 16px;
            font-size: 0.82rem;
            vertical-align: middle;
          }
          .sm-url a {
            color: #16b2dc;
            text-decoration: none;
            font-weight: 500;
            word-break: break-all;
          }
          .sm-url a:hover { text-decoration: underline; }
          .sm-meta {
            color: #888;
            font-size: 0.75rem;
            white-space: nowrap;
          }
          .sm-priority {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 50px;
            font-size: 0.7rem;
            font-weight: 700;
            white-space: nowrap;
          }
          .pri-high   { background: #e6f8fd; color: #0e8aaa; border: 1px solid #b3e8f7; }
          .pri-mid    { background: #f0f8fc; color: #1a7fa0; border: 1px solid #c8e8f5; }
          .pri-low    { background: #f5f5f5; color: #999;    border: 1px solid #e0e0e0; }

          /* ── Footer ── */
          .sm-footer {
            text-align: center;
            padding: 32px 20px;
            font-size: 0.75rem;
            color: #aaa;
            border-top: 1px solid #e8e8e8;
          }
          .sm-footer a { color: #16b2dc; text-decoration: none; }
          .sm-footer a:hover { text-decoration: underline; }

          @media (max-width: 600px) {
            .sm-header h1 { font-size: 1.3rem; }
            .sm-table thead th:nth-child(3),
            .sm-table td:nth-child(3) { display: none; }
          }
        </style>
      </head>
      <body>

        <div class="sm-header">
          <img src="/static/Pictures/john-ngor-deng-garang-logo.png" alt="John Ngor Deng Garang"/>
          <h1>XML Sitemap</h1>
          <p>johngarang.com</p>
        </div>

        <div class="sm-container">

          <!-- Stats -->
          <div class="sm-stats">
            <div class="sm-stat">
              <div class="sm-stat-num"><xsl:value-of select="count(sm:urlset/sm:url)"/></div>
              <div class="sm-stat-label">Total URLs</div>
            </div>
            <div class="sm-stat">
              <div class="sm-stat-num"><xsl:value-of select="count(sm:urlset/sm:url[sm:priority &gt;= 0.9])"/></div>
              <div class="sm-stat-label">High Priority</div>
            </div>
            <div class="sm-stat">
              <div class="sm-stat-num"><xsl:value-of select="count(sm:urlset/sm:url[sm:changefreq = 'weekly'])"/></div>
              <div class="sm-stat-label">Updated Weekly</div>
            </div>
          </div>

          <!-- Table -->
          <table class="sm-table">
            <thead>
              <tr>
                <th style="width:55%">URL</th>
                <th>Last Modified</th>
                <th>Frequency</th>
                <th>Priority</th>
              </tr>
            </thead>
            <tbody>
              <xsl:for-each select="sm:urlset/sm:url">
                <tr>
                  <td class="sm-url">
                    <a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a>
                  </td>
                  <td class="sm-meta"><xsl:value-of select="sm:lastmod"/></td>
                  <td class="sm-meta"><xsl:value-of select="sm:changefreq"/></td>
                  <td>
                    <xsl:choose>
                      <xsl:when test="sm:priority &gt;= 0.9">
                        <span class="sm-priority pri-high"><xsl:value-of select="sm:priority"/></span>
                      </xsl:when>
                      <xsl:when test="sm:priority &gt;= 0.7">
                        <span class="sm-priority pri-mid"><xsl:value-of select="sm:priority"/></span>
                      </xsl:when>
                      <xsl:otherwise>
                        <span class="sm-priority pri-low"><xsl:value-of select="sm:priority"/></span>
                      </xsl:otherwise>
                    </xsl:choose>
                  </td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>

        </div>

        <div class="sm-footer">
          <a href="https://johngarang.com">johngarang.com</a> ·
          Generated for search engines and human visitors ·
          <a href="https://www.sitemaps.org" target="_blank" rel="noopener">Sitemap Protocol</a>
        </div>

      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
