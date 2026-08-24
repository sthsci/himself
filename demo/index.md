---
title: "Elephes Sung"
subtitle: "Something of a scientist"
author: "King of the Clingenland"
author-url: "https://github.com/ElephesSung"
lang: en
# toc-title: "Contents"
# description-meta: "Personal academic website of Elephes Sung / Fanxin Song at Imperial College London"
# keywords:
#   - bioinformatics
#   - life sciences
#   - Imperial College London
---


## About

<table class="about-card">
  <tr>
    <td class="width-min about-photo-cell">
      <figure class="bw-photo about-photo">
        <img src="demo/profile_2.JPG" alt="Elephes Sung" />
        <figcaption>print("hello")</figcaption>
      </figure>
    </td>

    <td class="width-auto about-copy">
      <p>I am currently a PhD student in Life Sciences at Imperial College, with a research interest in <strong>mathematical biophysics and immunology</strong>.</p>

      <p>Previously, I completed an MRes in Systems and Synthetic Biology, also at Imperial College. Even prior to that, I got my bachelor’s degree in Nanomaterials and Nanotechnology.</p>

      <p>Approximately 84% of people mispronounce my name on first reading, while 52.1% confidently assume it is Greek. Neither observation is especially concerning: you are entirely welcome to pronounce it however you wish.</p>

      <p>You can email me at <a href="mailto:eu23@ic.ac.uk?subject=Hello_from_webpage">eu23@ic.ac.uk</a></p>
    </td>
  </tr>
</table>

<br>

---

<br>

## Trajectory

This is a horizontal plot, scroll right to check it.

<figure class="trajectory">
<pre>
/*
            I need more quantitative                                                                                  
            & systematic methods to                                                                                   
            immunological mechanisms                                                                                  
                     │                                                                                                
  2019-2023          │       2023-2024                               2024-2028                                        
 ┌───────────────┐   │      ┌────────────────────┐                  ┌─────────────────────────────────────────┐       
 │ B.Eng.        ┼───┴─────►│ M.Res. Systems     ┼──────┬──────────►│ PhD in Life Sciences Research           │       
 │ Nanomaterials │          │ & Synthetic Biology│      │           │ President's Scholarship                 │       
 └┬──┬──────────┬┘          └─────────┬──────────┘      │           └──────┬──────────────────────────────────┘       
  │  └─────┬────┘                     │             in between:            │   Project 1. dynamics of interactions    
  │        │~3yrs                     │             ESA Hackthon           │          between killer immune cell      
  │        ▼                          ▼             Bayesian inference     │                     & target cells       
  │   UG project               Master's project       for astronauts'      │                                          
  │   Injectable Hydrogel      Agent-based modelling    health prediction  │   Project 2. dynamics of immune receptors
  │   NK cell delivery         NK cell-tumour                              │          & cell decision-making          
  │         cancer therapy             interactions                        │                                          
  ▼ ~1yr                                                                   │                                          
  lab intern                                                               small confidential project:                
  solar chemical                                                           Google Deepmind & Imperial College         
  battery                                                                                                             
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐      
│  TIMELINE                           TIMELINE                        TIMELINE                     TIMELINE    │      
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘      
 */
</pre>
</figure>

<br>

---

<br>


## Research and Development

My work connects experimental biology with quantitative modelling. These projects span Bayesian inference, research software, imaging analysis, simulation, and biomaterials development.

<br>

### Bayesian inference for immunology

<div class="project-stack">
<div class="project-panel">
<p class="project-kicker">Research framework and open-source software</p>

<figure class="project-figure project-figure-wide">
<img class="project-asset" src="demo/Bayes/figure_abstract.png" alt="Graphic abstract showing how BARRACUDA converts time-lapse imaging into single-cell kill-contact histories and tests population heterogeneity and longitudinal variation." />
<figcaption>BARRACUDA uses single-cell kill-contact histories to identify the mechanisms underlying variation in NK-cell cytotoxicity.</figcaption>
</figure>

<div class="project-copy">
<h4>BARRACUDA</h4>
<p><strong>Bayesian Analysis Resolving Randomness and Alternative Causes Underlying Differential Activity</strong> is a quantitative framework for identifying why natural killer (NK) cell cytotoxic behaviour varies between individual cells. It combines event-count models with ordered contact-kill histories to distinguish stochastic encounters and killing decisions from stable cell-to-cell differences, donor effects, and changes induced by previous interactions.</p>

<p>Applied to time-lapse imaging of untreated, rituximab-treated, and CC-96673-treated NK cells, the framework found continuous heterogeneity across conditions while revealing distinct treatment mechanisms: rituximab primarily increased killing efficiency, whereas CC-96673 reduced cell-to-cell variability and produced a more homogeneous cytotoxic response.</p>

<div class="project-actions">
<a class="icon-button" href="https://github.com/sthsci/Barracuda" target="_blank" rel="noopener noreferrer">GitHub</a>
<a class="icon-button" href="https://barracuda.clingenland.science/" target="_blank" rel="noopener noreferrer">Web app</a>
<a class="icon-button" href="https://sthsci.github.io/Barracuda/" target="_blank" rel="noopener noreferrer">Python API</a>
</div>
</div>
</div>

<article class="project-panel project-panel-split">
<figure class="project-figure bw-photo">
<img class="project-asset" src="demo/Bayes/redshift.png" alt="Summary slide from Redshift, a hackathon project modelling astronaut immune health with cytokine dynamics and a normalized resilience factor." />
<figcaption>Redshift: a compact cytokine-based immune-risk model for spaceflight.</figcaption>
</figure>
<div class="project-copy">
<h4>Redshift</h4>
<p>A brief Bayesian/ABC modelling project from the first European Space Agency hackathon, building a compact cytokine-based resilience factor for astronaut immune health.</p>
<p>Our team initially won, though the medal was later rescinded for administrative and political reasons.</p>
</div>
</article>
</div>

<br>

### Crappy softwares: imaging analysis and simulators

<div class="project-stack">
<article class="project-panel">
<figure class="project-figure bw-photo">
<video class="project-asset" autoplay muted loop playsinline preload="metadata">
<source src="demo/software/animation_Tu_12.mp4" type="video/mp4" />
<img src="demo/software/animation_Tu_12.gif" alt="Animated CytotoxicVision output showing a target cell, nearby immune cells, and fluorescence traces over time." />
</video>
<figcaption>Single-cell dynamics from CytotoxicVision.</figcaption>
</figure>
<div class="project-copy">
<h4>CytotoxicVision</h4>
<p>A small but useful imaging pipeline for analysing time-lapse fluorescence microscopy data of NK-cell interactions with 721.221 target cells. Demo data from Dr Cathal Hosty from the Dan Davis lab.</p>
<p>The current version is still more of a demonstration framework than a polished package, but it already produces interpretable single-cell and population-level readouts.</p>
<p><strong>Repository:</strong> <a href="https://github.com/ElephesSung/CytotoxicVision" target="_blank" rel="noopener noreferrer">github.com/ElephesSung/CytotoxicVision</a></p>
</div>
</article>

<article class="project-panel project-panel-split">
<figure class="project-figure bw-photo">
<video class="project-asset" autoplay muted loop playsinline preload="metadata">
<source src="demo/software/vis_test.mp4" type="video/mp4" />
<img src="demo/software/vis_test.gif" alt="Animated MantiShrimp simulation showing killer and target cells moving within a bounded region over time." />
</video>
<figcaption>Agent-based killer-target simulation from MantiShrimp.</figcaption>
</figure>
<div class="project-copy">
<h4>MantiShrimp</h4>
<p>A Python package for off-lattice, two-dimensional agent-based modelling of killer immune cell-target cell interactions. It combines cell migration and Hookean mechanics with contact formation, probabilistic killing, target death, and cell-state dynamics, and includes Bayesian event-count models for inference from per-cell contacts or kills.</p>
<div class="project-actions">
<a class="icon-button" href="https://github.com/sthsci/MantiShrimp" target="_blank" rel="noopener noreferrer">GitHub</a>
<a class="icon-button" href="https://pypi.org/project/mantishrimp/" target="_blank" rel="noopener noreferrer">PyPI</a>
<a class="icon-button" href="https://doi.org/10.5281/zenodo.21908641" target="_blank" rel="noopener noreferrer">Zenodo DOI</a>
</div>
</div>
</article>
</div>

<br>

### Injectable Hydrogel

<div class="project-panel">
<div class="hydrogel-compare">
<figure class="project-figure bw-photo">
<video class="project-asset" autoplay muted loop playsinline preload="metadata">
<source src="demo/hydrogel/IMG_2881_bw.mp4" type="video/mp4" />
<img src="demo/hydrogel/IMG_2881_bw.gif" alt="Left: Demonstration of a shape-memory hydrogel scaffold being compressed for injection and recovering its shape afterward." />
</video>
</figure>
<div class="hydrogel-side">
<figure class="project-figure bw-photo">
<img class="project-asset" src="demo/hydrogel/IMG_3742.png" alt="Up: Scanning electron microscopy (SEM) image showing the interconnected porous microstructure of the hydrogel scaffold." />
</figure>
<div class="hydrogel-caption-block">
<p>← Injectable shape-memory hydrogel (gelatin) during compression and recovery.</p>
<p>↑ SEM view of the porous scaffold architecture.</p>
</div>
</div>
</div>

<details>
<summary>porous cryogel</summary>
<p>This was a biomaterials project I reproduced during my undergraduate studies, based on the injectable shape-memory scaffold reported by Bencherif and colleagues. The concept was simple but elegant: to create a porous hydrogel that could be compressed, injected through a syringe, and then recover its original structure after injection.</p>

<p>In their work, the porous architecture was generated through slow covalent crosslinking at low temperature. Ice crystals formed during the crosslinking process occupied space within the material and later served as pore templates.</p>

<p>Later, my colleagues and I developed a related approach for producing an ionically crosslinked porous alginate hydrogel. We first froze and lyophilised the alginate precursor, then immersed it in a calcium-ion solution to induce crosslinking. This produced a highly similar porous structure, while also preserving the material’s injectable behaviour.</p>

<p>Our original aim was to load NK cells into the hydrogel and use it as a delivery platform for solid tumours. Because of COVID and a few other unavoidable disruptions, I never managed to complete the bioengineering part of the project. It was a slightly frustrating ending.</p>

<p><strong>Reference:</strong> Sidi A. Bencherif, R. Warren Sands, Deen Bhatta, et al. “Injectable preformed scaffolds with shape-memory properties.” <em>Proceedings of the National Academy of Sciences</em> 109(48): 19590-19595 (2012). <a href="https://doi.org/10.1073/pnas.1211516109" target="_blank" rel="noopener noreferrer">doi.org/10.1073/pnas.1211516109</a></p>
</details>
</div>

<br>

---

<br>

## Publications

<p>
  <a class="icon-button scholar-button" href="https://scholar.google.com/citations?user=HcFouHYAAAAJ&hl=en" target="_blank" rel="noopener noreferrer" aria-label="Open Google Scholar profile">
    <span>Google Scholar</span>
  </a>
</p>



<details>
<summary> Mathematical Biophysics </summary>
<p>coming soon...</p>
</details>






<details>

<summary>Nanomaterials & Drug Delivery</summary>
<p>
<table class="pub-cards">
  <tr>
    <td class="width-auto">
      <p><strong>Review</strong></p>
      <p>Precision Medicine: The Road to In Vivo Synthetic Therapeutic Agent.</p>
      <p>Yang‐Bao Miao, Zhao Wang, <strong>Fan-Xin Song</strong>, Renchi Gao, Zheng Deng, Guohui Zhang</p>
      <p><em>Advanced Functional Materials</em>, Vol. 35, Issue 47, p. 2510183 (2025)</p>
      <p><a href="https://doi.org/10.1002/adfm.202510183">Read more</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Review</strong></p>
      <p>Recent Progress in Nanomaterial-Based Biosensors and Theranostic Nanomedicine for Bladder Cancer.</p>
      <p><strong>Fan-Xin Song</strong>, Xiaojian Xu, Hengze Ding, Le Yu, Haochen Huang, Jinting Hao, Chenghao Wu, Rui Liang, Shaohua Zhang</p>
      <p><em>Biosensors</em>, Vol. 13, Issue 1, p. 106 (2023)</p>
      <p><a href="https://doi.org/10.3390/bios13010106">Read more</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Article</strong></p>
      <p>Achieving Precise Non-Invasive ROS Spatiotemporal Manipulation for Colon Cancer Immunotherapy.</p>
      <p>Yang-Bao Miao, Hong-Xia Ren, Guohui Zhang, <strong>Fan-Xin Song</strong>, Weixin Liu, Yi Shi</p>
      <p><em>Chemical Engineering Journal</em>, Vol. 481, p. 148520 (2024)</p>
      <p><a href="https://doi.org/10.1016/j.cej.2024.148520">Read more</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Article</strong></p>
      <p>Tailoring a Luminescent Metal–Organic Framework Precise Inclusion of Pt-Aptamer Nanoparticle for Noninvasive Monitoring Parkinson's Disease.</p>
      <p>Yang-Bao Miao, Hong-Xia Ren, Qilong Zhong, <strong>Fan-Xin Song</strong></p>
      <p><em>Chemical Engineering Journal</em>, Vol. 441, p. 136009 (2022)</p>
      <p><a href="https://doi.org/10.1016/j.cej.2022.136009">Read more</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Article</strong></p>
      <p>All-in-One, Solid-State, Solar-Powered Electrochemical Cell.</p>
      <p>Yu Zhao, Chenyang Li, <strong>Fan-Xin Song</strong>, Yi Li, Yan Liu, Yajie Zhao, Xiaohong Zhang, Yu Zhao, Zhenhui Kang</p>
      <p><em>ACS Applied Materials & Interfaces</em>, Vol. 12, Issue 51, pp. 57182–57189 (2020)</p>
      <p><a href="https://doi.org/10.1021/acsami.0c19167">Read more</a></p>
    </td>
  </tr>
</table>
</p>

</details>







<!-- 
## The Basics

This document uses a few extra classes here and there, but mostly it's just markup.
This, for instance, is a regular paragraph.

Look at this horizontal break:

<hr>

Lovely. We can hide stuff in the `<details`> element:

<details>
<summary>A short summary of the contents</summary>
<p>Hidden gems.</p>
</details>

## Lists

This is a plain old bulleted list:

* Banana
* Paper boat
* Cucumber
* Rocket

Ordered lists look pretty much as you'd expect:

1. Goals
1. Motivations
    1. Intrinsic
    1. Extrinsic
1. Second-order effects

It's nice to visualize trees.
This is a regular unordered list with a `tree` class:

<ul class="tree"><li><p style="margin: 0;"><strong>/dev/nvme0n1p2</strong></p>

* usr                               
    * local                         
    * share                         
    * libexec                       
    * include                       
    * sbin                          
    * src                           
    * lib64                         
    * lib                           
    * bin                           
    * games                         
        * solitaire
        * snake
        * tic-tac-toe
    * media                         
* media                             
* run                               
* tmp                               

</li></ul>

## Tables

We can use regular tables that automatically adjust to the monospace grid.
They're responsive. 

<table>
<thead>
  <tr>
    <th class="width-min">Name</th>
    <th class="width-auto">Dimensions</th>
    <th class="width-min">Position</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Boboli Obelisk</td>
    <td>1.41m &times; 1.41m &times; 4.87m</td>
    <td>43°45'50.78"N 11°15'3.34"E</td>
  </tr>
  <tr>
    <td>Pyramid of Khafre</td>
    <td>215.25m &times; 215.25m &times; 136.4m</td>
    <td>29°58'34"N 31°07'51"E</td>
  </tr>
</tbody>
</table>

Note that only one column is allowed to grow.

## Forms

Here are some buttons:

<nav>
    <button>Reset</button>
    <button>Save</button>
</nav>

And inputs:

<form class="grid">
<label>First name <input type="text" placeholder="Placeholder..." /></label>
<label>Last name <input type="text" placeholder="Text goes here..." /></label>
<label>Age <input type="text" value="30" /></label>
</form>

And radio buttons:

<form class="grid">
<label><input name="radio" type="radio" /> Option #1</label>
<label><input name="radio" type="radio" /> Option #2</label>
<label><input name="radio" type="radio" /> Option #3</label>
</form>

## Grids

Add the `grid` class to a container to divide up the horizontal space evenly for the cells.
Note that it maintains the monospace, so the total width might not be 100%.
Here are six grids with increasing cell count:

<div class="grid"><input readonly value="1" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /><input readonly value="4" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /><input readonly value="4" /><input readonly value="5" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /><input readonly value="4" /><input readonly value="5" /><input readonly value="6" /></div>

If we want one cell to fill the remainder, we set `flex-grow: 1;` for that particular cell.

<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3!" style="flex-grow: 1;" /><input readonly value="4" /><input readonly value="5" /><input readonly value="6" /></div>

## ASCII Drawings

We can draw in `<pre>` tags using [box-drawing characters](https://en.wikipedia.org/wiki/Box-drawing_characters):

```
╭─────────────────╮
│ MONOSPACE ROCKS │
╰─────────────────╯
```

To have it stand out a bit more, we can wrap it in a `<figure>` tag, and why not also add a `<figcaption>`.

<figure>
<pre>
┌───────┐ ┌───────┐ ┌───────┐
│Actor 1│ │Actor 2│ │Actor 3│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │    
    │         │  msg 1  │    
    │         │────────►│    
    │         │         │    
    │  msg 2  │         │    
    │────────►│         │    
┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│Actor 1│ │Actor 2│ │Actor 3│
└───────┘ └───────┘ └───────┘</pre>
<figcaption>Example: Message passing.</figcaption>
</figure>

Let's go wild and draw a chart!

<figure><pre>
                      Things I Have
                                              
    │                                     ████ Usable
15  │
    │                                     ░░░░ Broken
    │
12  │             ░            
    │             ░            
    │   ░         ░              
 9  │   ░         ░              
    │   ░         ░              
    │   ░         ░                    ░
 6  │   █         ░         ░          ░
    │   █         ░         ░          ░
    │   █         ░         █          ░
 3  │   █         █         █          ░
    │   █         █         █          ░
    │   █         █         █          ░
 0  └───▀─────────▀─────────▀──────────▀─────────────
      Socks     Jeans     Shirts   USB Drives
</pre></figure>

## Media

Media objects are supported, like images and video:

![A room in an old French castle (2024)](demo/castle.jpg)

![[The Center of the Web (1914), Wikimedia](https://en.wikisource.org/wiki/Page:The_Center_of_the_Web_(1914).webm/11)](https://upload.wikimedia.org/wikipedia/commons/e/e0/The_Center_of_the_Web_%281914%29.webm)

They extend to the width of the page, and add appropriate padding in the bottom to maintain the monospace grid.

## Discussion

That's it for now.
I've very much enjoyed making this, pushing my CSS chops and having a lot of fun with the design.
If you like it or even decide to use it, please [let me know](https://x.com/owickstrom).

The full source code is here: [github.com/owickstrom/the-monospace-web](https://github.com/owickstrom/the-monospace-web)

Finally, a massive shout-out to [U.S. Graphics Company](https://x.com/usgraphics) for all the inspiration. -->
