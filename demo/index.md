---
title: "Elephes Sung"
subtitle: "Natural killer cells and their targets"
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


[Watch my science animations](animations/index.html){.icon-button}

## About me {#about}

<table class="about-card">
  <tr>
    <td class="width-min about-photo-cell">
      <figure class="bw-photo about-photo">
        <img src="demo/profile_2.JPG" alt="Portrait of Elephes Sung" />
        <figcaption>Hello, I’m Elephes.</figcaption>
      </figure>
    </td>

    <td class="width-auto about-copy">
      <p>I’m a PhD student in Life Sciences at Imperial College London. I work in <strong>mathematical biophysics and immunology</strong>, studying why some targets survive an encounter with a natural killer (NK) cell and others do not.</p>

      <p>I studied Nanomaterials and Nanotechnology as an undergraduate, then completed an MRes in Systems and Synthetic Biology at Imperial.</p>

      <p>Email me at <a href="mailto:eu23@ic.ac.uk?subject=Hello_from_webpage">eu23@ic.ac.uk</a>.</p>
    </td>
  </tr>
</table>

<br>

---

<br>

## Education and research timeline {#trajectory}

I turned from materials engineering to mathematical modelling because I wanted to understand how immune cells work. Scroll right to follow the timeline.

<figure class="trajectory">
<pre>
 2019–2023                         2023–2024                           2024–2028
┌─────────────────────────────┐   ┌───────────────────────────────┐   ┌──────────────────────────────────────────┐
│ B.Eng. in Nanomaterials     │──►│ MRes in Systems               │──►│ PhD in Life Sciences Research            │
│ and Nanotechnology          │   │ and Synthetic Biology         │   │ President’s Scholarship                  │
└─┬───────────────────────────┘   └─┬─────────────────────────────┘   └─┬────────────────────────────────────────┘
  ├─ Lab internship (~1 year)       ├─ Master’s project                 ├─ Project 1: How killer immune cells
  │  Solar chemical battery         │  Agent-based modelling of         │  interact with target cells
  │                                 │  NK cell–tumour interactions      │
  └─ Undergraduate project          │                                   ├─ Project 2: Immune receptor dynamics
     (~3 years)                     └─ Before my PhD: ESA hackathon     │  and how cells make decisions
     Injectable hydrogel for           Bayesian inference for           │
     NK cell delivery in               astronaut health prediction      └─ Small confidential project with
     cancer therapy                                                        Google DeepMind and Imperial College
</pre>
</figure>

<br>

---

<br>


## Research projects {#research-and-development}

Time-lapse microscopy lets me follow an immune cell from one target to the next. I write software to analyse those encounters and use Bayesian models and simulations to interpret them. My earlier work in biomaterials asked how an injectable gel might carry immune cells into a solid tumour.

<br>

### Bayesian models of immune function {#bayesian-inference-for-immunology}

<div class="project-stack">
<div class="project-panel">
<p class="project-kicker">Open-source software for single-cell analysis</p>

<div class="project-copy">
<h4>BARRACUDA</h4>
<figure class="project-figure project-figure-inset">
<img class="project-asset" src="demo/Bayes/figure_abstract.png" alt="A microscopy image leads to a sequence of lethal and non-lethal contacts for one NK cell. The lower panels compare variation between cells with changes in one cell over successive contacts." />
<figcaption>Each NK cell has a history: which targets it touched, in what order, and which of those targets died.</figcaption>
</figure>

<p>A high kill count alone cannot tell us whether an NK cell met more targets or was more likely to kill the ones it met. We developed BARRACUDA (<strong>Bayesian Analysis Resolving Randomness and Alternative Causes Underlying Differential Activity</strong>) to study that distinction. We use event-count models alongside each cell’s sequence of contacts and kills to test how much variation chance can explain. We also test for persistent differences between cells, differences between donors and changes within a cell after earlier encounters.</p>

<p>Our analysis of time-lapse recordings suggested a continuum of NK-cell killing activity in untreated samples and in both treatment conditions. Rituximab was associated mainly with higher killing efficiency. With CC-96673, killing activity varied less from cell to cell.</p>

<div class="project-actions">
<a class="icon-button" href="https://www.biorxiv.org/content/10.64898/2026.09.16.752048v1.abstract" target="_blank" rel="noopener noreferrer">Read the preprint</a>
<a class="icon-button" href="https://github.com/sthsci/Barracuda" target="_blank" rel="noopener noreferrer">BARRACUDA on GitHub</a>
<a class="icon-button" href="https://barracuda.clingenland.science/" target="_blank" rel="noopener noreferrer">Open the web app</a>
<a class="icon-button" href="https://sthsci.github.io/Barracuda/" target="_blank" rel="noopener noreferrer">Python API reference</a>
</div>
</div>
</div>

<article class="project-panel project-panel-split">
<figure class="project-figure bw-photo">
<img class="project-asset" src="demo/Bayes/redshift.png" alt="Curves show how activating and inhibitory cytokine concentrations change in the model. A second plot illustrates the resulting resilience factor before, during and after spaceflight." />
<figcaption>Redshift summarises the balance between activating and inhibitory cytokines as a normalised resilience factor.</figcaption>
</figure>
<div class="project-copy">
<h4>Redshift</h4>
<p>At the first European Space Agency hackathon, our team built Redshift to study how spaceflight might affect astronauts’ immune function. We used approximate Bayesian computation (ABC) to estimate how cytokine concentrations change over time.</p>
<p>Our team won the hackathon, but the medal was later withdrawn. My understanding is that the reasons were administrative and political.</p>
</div>
</article>
</div>

<br>

### Software for cell imaging and simulation {#crappy-softwares-imaging-analysis-and-simulators}

<div class="project-stack">
<article class="project-panel">
<figure class="project-figure bw-photo">
<video class="project-asset" autoplay muted loop playsinline preload="metadata">
<source src="demo/software/animation_Tu_12.mp4" type="video/mp4" />
<img src="demo/software/animation_Tu_12.gif" alt="Microscopy images follow a target cell and nearby immune cells. Beside them, a plot shows fluorescence intensity in the target over time." />
</video>
<figcaption>In this target cell, the Calcein Green AM signal falls as the TO-PRO-3 signal rises.</figcaption>
</figure>
<div class="project-copy">
<h4>CytotoxicVision</h4>
<p>CytotoxicVision analyses time-lapse fluorescence microscopy of NK cells interacting with 721.221 target cells. Dr Cathal Hosty in the Dan Davis lab provided the example recordings.</p>
<p>The software is a prototype. It pairs images of individual cells with their fluorescence traces and summarises measurements across the cell population.</p>
<p><a href="https://github.com/ElephesSung/CytotoxicVision" target="_blank" rel="noopener noreferrer">CytotoxicVision source code on GitHub</a></p>
</div>
</article>

<article class="project-panel project-panel-split">
<figure class="project-figure bw-photo">
<video class="project-asset" autoplay muted loop playsinline preload="metadata">
<source src="demo/software/vis_test.mp4" type="video/mp4" />
<img src="demo/software/vis_test.gif" alt="Simulated killer cells move among a cluster of targets inside a square boundary. The legend distinguishes killer cells, live targets and dead targets." />
</video>
<figcaption>Each marker is a cell. The simulation follows its movement and records when a target dies.</figcaption>
</figure>
<div class="project-copy">
<h4>MantiShrimp</h4>
<p>MantiShrimp is a Python package for simulating encounters between killer immune cells and their targets. Each cell is an agent that moves in two dimensions without a fixed grid. This off-lattice model uses Hookean mechanics for cell interactions and allows cells to change state. Killing is probabilistic, so a target can survive contact. The package also fits Bayesian event-count models to the number of contacts or kills recorded for each cell.</p>
<div class="project-actions">
<a class="icon-button" href="https://github.com/sthsci/MantiShrimp" target="_blank" rel="noopener noreferrer">MantiShrimp on GitHub</a>
<a class="icon-button" href="https://pypi.org/project/mantishrimp/" target="_blank" rel="noopener noreferrer">Package on PyPI</a>
<a class="icon-button" href="https://doi.org/10.5281/zenodo.21908641" target="_blank" rel="noopener noreferrer">Zenodo record</a>
</div>
</div>
</article>
</div>

<br>

### Injectable hydrogels {#injectable-hydrogel}

<div class="project-panel">
<div class="hydrogel-compare">
<figure class="project-figure bw-photo">
<video class="project-asset" autoplay muted loop playsinline preload="metadata">
<source src="demo/hydrogel/IMG_2881_bw.mp4" type="video/mp4" />
<img src="demo/hydrogel/IMG_2881_bw.gif" alt="A gelatin scaffold is compressed and expands back to its original shape when released." />
</video>
</figure>
<div class="hydrogel-side">
<figure class="project-figure bw-photo">
<img class="project-asset" src="demo/hydrogel/IMG_3742.png" alt="Scanning electron micrograph of the hydrogel scaffold showing how its pores connect." />
</figure>
<div class="hydrogel-caption-block">
<p>In the animation, the gelatin hydrogel regains its shape after compression.</p>
<p>Scanning electron microscopy (SEM) shows where neighbouring pores connect.</p>
</div>
</div>
</div>

<details>
<summary>How we made the porous cryogel</summary>
<p>As an undergraduate, I reproduced the injectable shape-memory scaffold described by Bencherif and colleagues. Their porous hydrogel could be compressed to fit through a syringe and would regain its shape after injection.</p>

<p>In their method, ice crystals form as the gel slowly crosslinks through covalent bonds at low temperature. When the ice melts, the spaces the crystals occupied become pores.</p>

<p>My colleagues and I later made a version from alginate. We froze and lyophilised the precursor, then immersed it in a solution of calcium ions to form ionic crosslinks. The gel had a similar pore structure and could still pass through a syringe.</p>

<p>We wanted to load the gel with NK cells and deliver them to solid tumours. COVID and other disruptions cut the project short. It was frustrating to leave the cell-delivery work unfinished.</p>

<p><strong>Reference:</strong> Sidi A. Bencherif, R. Warren Sands, Deen Bhatta, et al. “Injectable preformed scaffolds with shape-memory properties.” <em>Proceedings of the National Academy of Sciences</em> 109(48): 19590-19595 (2012). <a href="https://doi.org/10.1073/pnas.1211516109" target="_blank" rel="noopener noreferrer">doi.org/10.1073/pnas.1211516109</a></p>
</details>
</div>

<br>

---

<br>

## Publications

<p>
  <a class="icon-button scholar-button" href="https://scholar.google.com/citations?user=HcFouHYAAAAJ&hl=en" target="_blank" rel="noopener noreferrer">
    <span>My Google Scholar profile</span>
  </a>
</p>



<details>
<summary>Mathematical biophysics</summary>
<table class="pub-cards">
  <tr>
    <td class="width-auto">
      <p><strong>Preprint</strong></p>
      <p>A Bayesian framework reveals heterogeneous and stochastic decision-making in NK cell cytotoxicity.</p>
      <p><strong>Elephes Sung</strong>, Cathal Hosty, Khodor S. Hazime, Leanne Peiser, Lara Stepan, Daniel M. Davis, Ruben Perez-Carrasco</p>
      <p><em>bioRxiv</em>, posted 22 September 2026</p>
      <p><a href="https://www.biorxiv.org/content/10.64898/2026.09.16.752048v1.abstract">Read the NK-cell preprint</a> · DOI: <a href="https://doi.org/10.64898/2026.09.16.752048">10.64898/2026.09.16.752048</a></p>
    </td>
  </tr>
</table>
</details>






<details>

<summary>Nanomaterials and drug delivery</summary>
<p>
<table class="pub-cards">
  <tr>
    <td class="width-auto">
      <p><strong>Review</strong></p>
      <p>Precision Medicine: The Road to In Vivo Synthetic Therapeutic Agent.</p>
      <p>Yang‐Bao Miao, Zhao Wang, <strong>Fan-Xin Song</strong>, Renchi Gao, Zheng Deng, Guohui Zhang</p>
      <p><em>Advanced Functional Materials</em>, Vol. 35, Issue 47, p. 2510183 (2025)</p>
      <p><a href="https://doi.org/10.1002/adfm.202510183">Read the review on in vivo synthesis</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Review</strong></p>
      <p>Recent Progress in Nanomaterial-Based Biosensors and Theranostic Nanomedicine for Bladder Cancer.</p>
      <p><strong>Fan-Xin Song</strong>, Xiaojian Xu, Hengze Ding, Le Yu, Haochen Huang, Jinting Hao, Chenghao Wu, Rui Liang, Shaohua Zhang</p>
      <p><em>Biosensors</em>, Vol. 13, Issue 1, p. 106 (2023)</p>
      <p><a href="https://doi.org/10.3390/bios13010106">Read the bladder cancer review</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Article</strong></p>
      <p>Achieving Precise Non-Invasive ROS Spatiotemporal Manipulation for Colon Cancer Immunotherapy.</p>
      <p>Yang-Bao Miao, Hong-Xia Ren, Guohui Zhang, <strong>Fan-Xin Song</strong>, Weixin Liu, Yi Shi</p>
      <p><em>Chemical Engineering Journal</em>, Vol. 481, p. 148520 (2024)</p>
      <p><a href="https://doi.org/10.1016/j.cej.2024.148520">Read the colon cancer immunotherapy study</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Article</strong></p>
      <p>Tailoring a Luminescent Metal–Organic Framework Precise Inclusion of Pt-Aptamer Nanoparticle for Noninvasive Monitoring Parkinson's Disease.</p>
      <p>Yang-Bao Miao, Hong-Xia Ren, Qilong Zhong, <strong>Fan-Xin Song</strong></p>
      <p><em>Chemical Engineering Journal</em>, Vol. 441, p. 136009 (2022)</p>
      <p><a href="https://doi.org/10.1016/j.cej.2022.136009">Read the Parkinson’s disease monitoring study</a></p>
    </td>
  </tr>
  <tr>
    <td class="width-auto">
      <p><strong>Article</strong></p>
      <p>All-in-One, Solid-State, Solar-Powered Electrochemical Cell.</p>
      <p>Yu Zhao, Chenyang Li, <strong>Fan-Xin Song</strong>, Yi Li, Yan Liu, Yajie Zhao, Xiaohong Zhang, Yu Zhao, Zhenhui Kang</p>
      <p><em>ACS Applied Materials & Interfaces</em>, Vol. 12, Issue 51, pp. 57182–57189 (2020)</p>
      <p><a href="https://doi.org/10.1021/acsami.0c19167">Read the solar-powered electrochemical cell study</a></p>
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
