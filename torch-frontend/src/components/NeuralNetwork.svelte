<script lang="ts">
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  interface NodeDatum {
    layerIdx: number;
    nodeIdx: number;
    x: number;
    y: number;
  }

  interface EdgeDatum {
    sourceIdx: number;
    targetIdx: number;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    weight: number;
  }

  const network = {
    layers: [
      { nodes: 3 },
      { nodes: 4 },
      { nodes: 2 },
    ],
  };

  const weights = [
    generateRandomWeights(3, 4),
    generateRandomWeights(4, 2),
  ];

  let svg: SVGSVGElement;

  // Generowanie losowych wag
  function generateRandomWeights(inputNodes: number, outputNodes: number): number[][] {
    return Array.from({ length: inputNodes }, () =>
      Array.from({ length: outputNodes }, () => parseFloat(Math.random().toFixed(2)))
    );
  }

  // Transformacja zoomowania
  let transform = d3.zoomIdentity;

  onMount(() => {
    const width = 800;
    const height = 500;
    const layerSpacing = width / (network.layers.length + 1);

    const svgSelection = d3.select(svg);
    svgSelection.selectAll('*').remove();

    const zoomGroup = svgSelection
      .append('g')
      .attr('class', 'zoom-group');

    svgSelection.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.5, 2]) // Skalowanie między 0.5 a 2x
        .on('zoom', (event) => {
          transform = event.transform; // Zachowaj aktualną transformację
          zoomGroup.attr('transform', transform);
        })
    );

    const nodes: d3.Selection<SVGCircleElement, NodeDatum, SVGGElement, unknown>[] = [];
    const edges: d3.Selection<SVGLineElement, EdgeDatum, SVGGElement, unknown>[] = [];
    const texts: d3.Selection<SVGTextElement, EdgeDatum, SVGGElement, unknown>[] = [];

    network.layers.forEach((layer, layerIdx) => {
      const ySpacing = height / (layer.nodes + 1);

      const nodeGroup = zoomGroup.append('g');
      const nodeSelection = nodeGroup
        .selectAll<SVGCircleElement, NodeDatum>('circle')
        .data(
          Array.from({ length: layer.nodes }).map((_, i) => ({
            layerIdx,
            nodeIdx: i,
            x: layerSpacing * (layerIdx + 1),
            y: ySpacing * (i + 1),
          }))
        )
        .enter()
        .append('circle')
        .attr('r', 15)
        .attr('fill', '#6ba3ff')
        .attr('stroke', '#003d99')
        .attr('stroke-width', 2)
        .attr('cx', (d) => d.x)
        .attr('cy', (d) => d.y)
        .on('mouseover', function () {
          d3.select(this).attr('fill', '#ffcc00');
        })
        .on('mouseout', function () {
          d3.select(this).attr('fill', '#6ba3ff');
        })
        .call(
          d3.drag<SVGCircleElement, NodeDatum>()
            .on('start', function () {
              d3.select(this).raise().attr('stroke', 'black');
            })
            .on('drag', (event, d) => {
              // Uwzględnienie transformacji zoomowania
              const [dx, dy] = transform.invert([event.x, event.y]);
              d.x = dx;
              d.y = dy;

              d3.select(event.sourceEvent.target)
                .attr('cx', d.x)
                .attr('cy', d.y);

              updateEdges();
            })
            .on('end', function () {
              d3.select(this).attr('stroke', '#003d99');
            })
        );

      nodes.push(nodeSelection);

      if (layerIdx < network.layers.length - 1) {
        const nextLayer = network.layers[layerIdx + 1];
        const nextYSpacing = height / (nextLayer.nodes + 1);

        const edgeGroup = zoomGroup.append('g');
        const edgeSelection = edgeGroup
          .selectAll<SVGLineElement, EdgeDatum>('line')
          .data(
            Array.from({ length: layer.nodes }).flatMap((_, sourceIdx) =>
              Array.from({ length: nextLayer.nodes }).map((_, targetIdx) => ({
                sourceIdx,
                targetIdx,
                x1: layerSpacing * (layerIdx + 1),
                y1: ySpacing * (sourceIdx + 1),
                x2: layerSpacing * (layerIdx + 2),
                y2: nextYSpacing * (targetIdx + 1),
                weight: weights[layerIdx][sourceIdx][targetIdx],
              }))
            )
          )
          .enter()
          .append('line')
          .attr('stroke', '#cccccc')
          .attr('stroke-width', 1)
          .attr('x1', (d) => d.x1)
          .attr('y1', (d) => d.y1)
          .attr('x2', (d) => d.x2)
          .attr('y2', (d) => d.y2);

        edges.push(edgeSelection);

        const textSelection = edgeGroup
          .selectAll<SVGTextElement, EdgeDatum>('text')
          .data(edgeSelection.data())
          .enter()
          .append('text')
          .attr('x', (d) => (d.x1 + d.x2) / 2)
          .attr('y', (d) => (d.y1 + d.y2) / 2)
          .attr('text-anchor', 'middle')
          .attr('font-size', '12px')
          .attr('fill', '#000')
          .text((d) => d.weight);

        texts.push(textSelection);
      }
    });

    function updateEdges() {
      edges.forEach((edgeSelection, layerIdx) => {
        edgeSelection.each(function (d) {
          const source = nodes[layerIdx].data()[d.sourceIdx];
          const target = nodes[layerIdx + 1].data()[d.targetIdx];

          d3.select(this)
            .attr('x1', source.x)
            .attr('y1', source.y)
            .attr('x2', target.x)
            .attr('y2', target.y);
        });
      });

      texts.forEach((textSelection, layerIdx) => {
        textSelection.each(function (d) {
          const source = nodes[layerIdx].data()[d.sourceIdx];
          const target = nodes[layerIdx + 1].data()[d.targetIdx];

          d3.select(this)
            .attr('x', (source.x + target.x) / 2)
            .attr('y', (source.y + target.y) / 2);
        });
      });
    }
  });
</script>

<style>
  .network-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px;
  }
  svg {
    border: 1px solid #ccc;
    background-color: #f9f9f9;
  }
</style>

<div class="network-container">
  <svg bind:this={svg} width="800" height="500"></svg>
</div>
