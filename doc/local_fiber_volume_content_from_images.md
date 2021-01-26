# Local Fiber Volume Content from Images

## Steps

- Take high quality images
  - Homogeneous specimen thickness
  - Homogeneous specimen surface condition
  - Homogeneous lightning conditions
  - The higher the resolution, the better
- Convert image to representative gray value matrix (think about transforms / filter / gamma / ...)
- Define mapping `map` from gray value `g` to fiber volume content `c`
  - Idea:
    - mean = integral fiber volume content of specimen
    - lower bound = neat resin specimen of identical thickness
  - Steps
    - use arithmetic mean
    - map:g -> c is linear
      - map(g) = a g + b
    - map(mean_over_specimen(g)) = mean_over_specimen(c) = known from manufacturing
    - map(min_over_specimen(g)) = 0

```

Light intensity:

    | -------------|--------------------------- |
 lower bound      mean                   upper bound

```

## Discussion 
Advantages of optical measurement of local fiber volume content

- cheap
- flexible
- high resolution

Thoughts on practical implementation

- Homogeneous lightning conditions
- Use complete range of light intensity of camera
- lower bound for neat resin (watch specimen thickness)
- Coordinate system identical to other measurements
  - Do not rotate specimen relative to placement in DIC and...
  - Mark specimen axis (Think about misalignment of camera relative to specimen plane)
  - [Mark center of specimen]

Choose marker variant 001 shown below where each `o` marks a GOM-marker

```
 001
                                        |
                            |-----------------------|
                            | arm 4     |           |
                            |                       |
                            |           |           |
                            |                       |
                            |           |           |
                            |                       |
        --------------------|  ___________________  |--------------------
        | arm 3               |         o         |              arm 1  |
        |                     |                   |                     |
        |                     |                   |                     |
      - |  - - - - - - - - -  |o        o        o|  - - - - - - - - -  | -
        |                     |                   |                     |
        |                     |                   |                     |
        |                     |_________o_________|                     |
        --------------------|                       |--------------------
                            |                       |
                            |           |           |
                            |                       |
                            |           |           |
                            |                       |
                            | arm 2     |           |
                            |-----------------------|
                                        |
```
