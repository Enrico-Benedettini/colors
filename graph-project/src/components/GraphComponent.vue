<template>
  <div class="p-6">
    <div class="mb-8 flex w-3/4 mx-auto justify-center items-center p-6 bg-gray-100 rounded-md">
      <div class="text-center">
        <h2 class="text-2xl font-bold text-gray-800">Graph Coloring Problem</h2>
        <p class="mt-4 text-lg text-gray-700">
          Companies printing maps are always trying to save money by buying the smallest amount of ink cartridge:
          given a map, they want to know if it is possible to print the map with <strong>k</strong> colors.
          Given an undirected graph <strong>G = (V, E)</strong> and an integer <strong>k</strong>,
          is there a way to color the vertices with <strong>k</strong> colors such that adjacent vertices are colored differently?
        </p>
      </div>
      <img src="/color.png" alt="Problem Description" class="w-1/4 ml-4">
    </div>

    <div class="flex justify-center items-center mb-6">
  <div class="justify-center w-1/4 space-y-4">
    <div>
      <label for="nodeCount" class="block text-sm font-medium text-gray-700">Number of Nodes:</label>
      <input id="nodeCount" type="number" v-model.number="nodeCount" @change="updateGraph" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
    </div>

    <div>
      <label for="edges" class="block text-sm font-medium text-gray-700">Edges (format: source-target, e.g., 1-2; 2-3):</label>
      <input id="edges" type="text" v-model="edgesInput" @change="updateGraph" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
    </div>

    <div>
      <label for="colorNumber" class="block text-sm font-medium text-gray-700">Number of Colors:</label>
      <input id="colorNumber" type="number" v-model.number="colorNumber" @change="updateGraph" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
    </div>

    <div>
      <h2 class="text-sm font-medium text-gray-700">Or File Upload:</h2>
      <label for="fileInput" class="block text-sm font-medium text-gray-700">File TXT input:</label>
      <input id="fileInput" type="file" @change="handleFileUpload" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
    </div>

    <div class="flex justify-center mt-4">
      <button @click="submit" class="px-4 py-2 bg-indigo-600 text-white font-medium rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
        Resolve Sat Problem
      </button>
    </div>
  </div>

  <div class="flex space-x-4 ml-4 justify-center">
    <div class="p-4 border border-gray-300 rounded-md shadow-sm" ref="chartContainer1"></div>
    <div v-if="this.result" class="p-4 border border-gray-300 rounded-md shadow-sm">
      <p class="text-lg font-medium text-gray-700 text-center mb-4">{{ result.status.toUpperCase() }}</p>
      <div ref="chartContainer2"></div>
    </div>
  </div>
</div>

<div v-if="result" class="mt-6 text-center">
  <p class="text-lg font-medium text-gray-700">{{ result.message }}</p>
</div>

  </div>
</template>




<script>
import * as d3 from 'd3';

export default {
  name: 'GraphComponent',

  data() {
    return {
      nodes: [],
      edges: [],
      nodeCount: 6,
      edgesInput: "1-5; 4-5; 4-6; 3-2; 5-2; 1-2; 3-4",
      colorNumber: 3,
      nodeColors: {},
      result: null
    };
  },

  mounted() {
    this.initializeGraph();
  },

  methods: {
    initializeGraph() {
      this.updateNodes();
      this.updateEdges();
      this.createCharts();
    },

    updateNodes() {
      const currentIds = new Set(this.nodes.map(node => node.id));
      const newIds = new Set([...Array(this.nodeCount).keys()].map(x => x + 1));

      this.nodes = this.nodes.filter(node => newIds.has(node.id));

      newIds.forEach(id => {
        if (!currentIds.has(id)) {
          this.nodes.push({ id });
        }
      });
    },

    updateEdges() {
      const newEdges = this.edgesInput.split(';').map(pair => {
        const [source, target] = pair.split('-').map(Number);
        return { source, target };
      });

      this.edges = newEdges.filter(edge =>
        this.nodes.find(node => node.id === edge.source) &&
        this.nodes.find(node => node.id === edge.target)
      );
    },

    createCharts() {
      this.createChart(this.$refs.chartContainer1, false);
      if (this.result) {
        this.createChart(this.$refs.chartContainer2, true);
      }
    },

    createChart(container, colorNodes) {
      const margin = { top: 30, right: 30, bottom: 30, left: 30 };
      const width = 300 - margin.left - margin.right; // Adjusted width
      const height = 300 - margin.top - margin.bottom; // Adjusted height

      d3.select(container).selectAll('svg').remove();

      const svg = d3.select(container)
          .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);

      const simulation = d3.forceSimulation(this.nodes)
          .force('link', d3.forceLink(this.edges).id(d => d.id).distance(100))
          .force('charge', d3.forceManyBody().strength(-50))
          .force('center', d3.forceCenter(width / 2, height / 2))
          .on('tick', ticked);

      const link = svg.append('g')
          .attr('class', 'links')
          .selectAll('line')
          .data(this.edges)
          .enter().append('line')
          .attr('stroke', '#999')
          .attr('stroke-opacity', 0.6)
          .attr('stroke-width', 2);

      const color = d3.scaleOrdinal(d3.schemeCategory10);

      const node = svg.append('g')
          .attr('class', 'nodes')
          .selectAll('circle')
          .data(this.nodes)
          .enter().append('circle')
          .attr('r', 10)
          .attr('fill', d => colorNodes ? color(this.nodeColors[d.id]) : 'black')
          .call(d3.drag()
              .on('start', dragstarted)
              .on('drag', dragged)
              .on('end', dragended));

      const text = svg.append('g')
          .attr('class', 'labels')
          .selectAll('text')
          .data(this.nodes)
          .enter().append('text')
          .text(d => d.id);

      function ticked() {
        link.attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node.attr('cx', d => d.x)
            .attr('cy', d => d.y);

        text.attr('x', d => d.x + 15)
            .attr('y', d => d.y + 5);
      }

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    },

    updateGraph() {
      this.updateNodes();
      this.updateEdges();
      this.createCharts();
    },

    isValidEdgeFormat(edgeString) {
      console.log(edgeString)
      const edgeFormat = /^\d+-\d+$/;
      return edgeFormat.test(edgeString);
    },

    submit() {
      const data = {
        node_count: this.nodeCount,
        edges: [],
        colors: this.colorNumber
      };
      if (this.edges.length === 0) {
        console.error('Error: No edges found');
        this.nodeCount = 0;
        this.updateGraph();
        return;
      }
      for (const edge of this.edges) {

        const edgeString = `${edge.source.id}-${edge.target.id}`;
        if (this.isValidEdgeFormat(edgeString)) {
          data.edges.push([edge.source.id, edge.target.id]);
        } else {
          console.error(`Error: Edge format is incorrect for edge ${edgeString}`);
        }
      }

      fetch('http://127.0.0.1:3000/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
          .then(response => response.json())
          .then(result => {
            this.result = result;
            this.nodeColors = result.solution;
            this.updateGraph();
            this.$nextTick(() => {
              this.createCharts();
            });
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Failed to fetch data: ' + error.message);
          });
    },


    handleFileUpload(event) {
      try {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = () => {
          const content = reader.result;
          const lines = content.split('\n');

          if (lines.length < 2) {
                console.error('Invalid file format');
                return;
              }

              this.nodeCount = Number(lines[0].trim());
              this.colorNumber = Number(lines[1].trim());

              const edges = lines.slice(2).map(line => line.trim());
              this.edgesInput = edges.join(';');

              this.updateGraph();
        };

        reader.readAsText(file);
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to read file: ' + error.message);
      }
    }
  },
  watch: {
    result(newResult, oldResult) {
      if (newResult !== oldResult) {
        this.$nextTick(() => {
          this.createCharts();
        });
      }
    }
  },

};
</script>

<style scoped>

</style>
