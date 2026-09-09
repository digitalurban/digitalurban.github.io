---
title: "Color Weather: A Data Watch Face for the Pebble Time 2"
date: 2026-09-09 11:15:00
slug: "color-weather-a-data-watch-face-for-the-pebble-time-2"
permalink: "/blog/2026/09/09/color-weather-a-data-watch-face-for-the-pebble-time-2/"
author: "Andy"
categories: ["Apps"]
tags: ["copilot", "Data", "github", "Pebble Watch", "Weather"]
excerpt: "Last October I made Just Weather, a black and white data face for the 144x168 screen of the Pebble 2 Duo. It did the job, but the Pebble Time 2, with its 200x228 screen and 64 colours was perfect for perhaps the next step…"
hero: "/assets/uploads/2026/09/color-weather-pebble-time-2.png"
---

<p>Last October I made <a href="https://www.digitalurban.org/blog/2025/10/30/just-weather-for-the-pebble-watch-making-a-data-watch-face/">Just Weather</a>, a black and white data face for the 144x168 screen of the Pebble 2 Duo. It did the job, but the Pebble Time 2, with its 200x228 screen and 64 colours was perfect for perhaps the next step.</p>
<p>That watch has now arrived. So, Just Weather was updated, to Color Weather.</p>
<figure class="wp-block-image size-large"><img src="/assets/uploads/2026/09/color-weather-pebble-time-2.png" alt="Color Weather running on a Pebble Time 2" />
<figcaption>Color Weather on the Pebble Time 2</figcaption></figure>
<h2>Introducing 'Color Weather'</h2>
<p>The idea is simple enough, and builds on a <a href="https://www.digitalurban.org/mqtt-weather/">web based dashboard</a> built over 10 years ago with a background set using the outside temperature.</p>
<figure class="wp-block-image size-large"><img src="/assets/uploads/2026/09/mqtt-weather-dashboard.png" alt="The MQTT weather dashboard, background set by the outside temperature" />
<figcaption>The original dashboard - same idea, rather more room for it.</figcaption></figure>
<p>The concept is same, but on a much smaller screen - the background is the temperature. Dark navy for a freeze, cobalt blue for a cold morning, through teal and a deep green in the mild middle, into tan and then a dark red when it's genuinely hot. Muted rather than bright - the duller palette turned out to work better on the watch.</p>
<figure class="wp-block-image size-large"><img src="/assets/uploads/2026/09/color-weather-temperature-bands.png" alt="The six Color Weather background bands and their hex values" />
<figcaption>The six background bands and their hex values.</figcaption></figure>
<ul>
 	<li>Below 0°C - <code>#000055</code> Oxford Blue</li>
 	<li>0 to 9°C - <code>#0055AA</code> Cobalt Blue</li>
 	<li>10 to 14°C - <code>#00AAAA</code> Tiffany Blue</li>
 	<li>15 to 19°C - <code>#005555</code> Midnight Green</li>
 	<li>20 to 24°C - <code>#AA5500</code> Windsor Tan</li>
 	<li>25°C and above - <code>#AA0000</code> Dark Candy Apple Red</li>
</ul>
<p>On top of the colour sits the usual data - time and a condition icon, city and temperature, conditions, pressure in millibars with its three hour trend, wind, rainfall, UV, and the day's step count and distance.</p>
<p>The face also keeps a rolling history and compares now against roughly three hours ago. A fall of 4 hPa or more puts <strong>Storm Warning</strong> on the screen, 6 hPa or more escalates it to <strong>Severe Storm</strong>, and the watch buzzes once when a warning first appears.</p>
<h2>Built with Copilot Again</h2>
<p>Same workflow as before - CloudPebble, VS Code in the browser and Copilot doing the heavy lifting on the C. Data is <a href="https://open-meteo.com/en/docs" target="_blank" rel="noopener">Open-Meteo</a> again, free and no key needed, with city names from Nominatim reverse geocoding and steps from Pebble's Health API. Everything refreshes every 15 minutes.</p>
<h2>Available Now</h2>
<ul>
 	<li><strong><a href="https://apps.repebble.com/color-weather_9c6ae3e3f93845168d890af1" target="_blank" rel="noopener">Color Weather on the Pebble Appstore</a></strong> - Pebble Time 2, currently version 2.1</li>
 	<li><strong><a href="https://github.com/digitalurban/color-weather-pebble" target="_blank" rel="noopener">Source and .pbw on GitHub</a></strong></li>
</ul>
<p>The mono version lives on for the Pebble 2 Duo - <a href="https://apps.rebble.io/en_US/application/69034d22d004720008412cf1" target="_blank" rel="noopener">Just Weather is still on the Rebble Appstore</a> - but if you have a Time 2, this is the one I wear...</p>
