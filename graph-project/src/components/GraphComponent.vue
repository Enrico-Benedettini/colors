<template>
  <div class="p-6">
    <div class="flex items-start mb-6">
      <!-- Input Section -->
      <div class="w-1/4 space-y-4">
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

        <div class="flex justify-center mt-4">
          <button @click="submit" class="px-4 py-2 bg-indigo-600 text-white font-medium rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Submit
          </button>
        </div>
      </div>

      <!-- Graph Containers -->
      <div class="flex-grow flex space-x-4 ml-4">
        <div class="w-1/2 p-4 border border-gray-300 rounded-md shadow-sm" ref="chartContainer1"></div>
        <div class="w-1/2 p-4 border border-gray-300 rounded-md shadow-sm" ref="chartContainer2"></div>
      </div>
    </div>

    <!-- Result Message -->
    <div v-if="result" class="mt-6 text-center">
      <p class="text-lg font-medium text-gray-700">{{ result }}</p>
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
      nodeColors: {}, // Store colors for second graph nodes
      result: null // Store result from backend
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

      // Remove nodes that no longer exist
      this.nodes = this.nodes.filter(node => newIds.has(node.id));

      // Add new nodes
      newIds.forEach(id => {
        if (!currentIds.has(id)) {
          this.nodes.push({ id });
        }
      });
    },

    updateEdges() {
      // Parse new edges input
      const newEdges = this.edgesInput.split(';').map(pair => {
        const [source, target] = pair.split('-').map(Number);
        return { source, target };
      });

      // Filter edges to only include those that have both nodes present
      this.edges = newEdges.filter(edge =>
          this.nodes.find(node => node.id === edge.source) &&
          this.nodes.find(node => node.id === edge.target)
      );
    },

    createCharts() {
      this.createChart(this.$refs.chartContainer1, false);
      this.createChart(this.$refs.chartContainer2, true);
    },

    createChart(container, colorNodes) {
      const margin = { top: 30, right: 30, bottom: 30, left: 30 };
      const width = 300 - margin.left - margin.right; // Adjusted width
      const height = 300 - margin.top - margin.bottom; // Adjusted height

      // Clear previous SVG
      d3.select(container).selectAll('svg').remove();

      const svg = d3.select(container)
          .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);

      // Setup the simulation with updated nodes and edges
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

      const node = svg.append('g')
          .attr('class', 'nodes')
          .selectAll('circle')
          .data(this.nodes)
          .enter().append('circle')
          .attr('r', 10)
          .attr('fill', d => colorNodes ? (this.nodeColors[d.id] || 'black') : 'black')
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

    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },

    updateGraph() {
      this.updateNodes();
      this.updateEdges();
      this.createCharts();
    },

    submit() {
      // Gather data to send to the backend
      const data = {
        nodeCount: this.nodeCount,
        edges: this.edges,
        colorNumber: this.colorNumber
      };

      // Send data to the backend
      fetch('/api/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
          .then(response => response.json())
          .then(result => {
            this.result = result.message; // Assuming backend returns { message: "some result" }
            this.updateGraph(); // Optionally update graph colors
          })
          .catch(error => {
            console.error('Error:', error);
          });
    }
  }
};
</script>

<style scoped>

</style>
