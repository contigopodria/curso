Vue.component('product-list', {
    data: function () {
        return {
            products: [], 
            productSelected: undefined,
            productIndexSelected: 0,
            timeDelete: 0,
            timeSave: 0
        }
    },
    mounted() {
        this.findAll()
    },
    methods: {
        findAll: function () {
            /* Creamos fetch que es una promesa*/
            fetch('http://localhost:5000/api/products/')
                .then(res => res.json())
                .then(res => this.products = res)
        },
        productDelete: function (product, index) {
            this.timeDelete = new Date().getTime()
            this.productSelected = product
            this.productIndexSelected = index
        },
        productSave: function () {
            this.productSelected = undefined
            this.timeSave = new Date().getTime()
        },
        productUpdate: function (product, index) {
            this.timeSave = new Date().getTime()
            this.productSelected = product
            this.productIndexSelected = index
        },
        eventProductDelete: function () {
            this.$delete(this.products.data, this.productIndexSelected) 
        },
        eventProductInsert: function (product) {
            this.products.data.push(product.data)
        },
        eventProductUpdate: function (product) {
            this.products.data[this.productIndexSelected].name = product.data.name
            this.products.data[this.productIndexSelected].price = product.data.price
            this.products.data[this.productIndexSelected].category = product.data.category
            this.products.data[this.productIndexSelected].category_id = product.data.category_id
        }
    },
     template:
     `
        <div>
            <div v-if="products.length==0">
                <h1>NO hay productos <button class="btn btn-outline-success mt-2 mb-2" @click="productSave"><i class="fa fa-plus"></i>Crear</button></h1>
            </div>
            <div v-else style="margin-top: 25px;">
                <h1>Productos <button class="btn btn-outline-success mt-2 mb-2" @click="productSave"><i class="fa fa-plus"></i>Crear</button></h1>
                <table id="products" class="table table-bordered table-striped table-hover table-sm">
                    <thead class="thead">
                        <tr>
                            <th style="text-align: center; min-width: 50px;">Código</th>
                            <th style="text-align: center; width: 70%;">Descripción</th>
                            <th style="text-align: center; min-width: 10px;">Precio</th>
                            <th style="text-align: center; min-width: 100px;">Categoría</th>
                            <th style="text-align: center; min-width: 100px;">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(product, index) in products.data">
                            <td style=" text-align: center;">{{ product.id }}</td>
                            <td style=" text-align: center;">{{ product.name }}</td>
                            <td style=" text-align: end;">{{ product.price }}</td>
                            <td style="text-align: center">{{ product.category }}</td>
                            <td style="text-align: center;">
                                <a @click="productUpdate(product, index)" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-file-pen"></i></a>
                                <button @click="productDelete(product, index)" :data-bs-name="product.name" :data-bs-id="product.id" class="btn btn-outline-danger btn-sm" style="margin-left: 10px;"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <product-delete @eventProductDelete="eventProductDelete" :time="timeDelete" :product="productSelected" ></product-delete>
            <product-save @eventProductUpdate="eventProductUpdate" @eventProductInsert="eventProductInsert" :time="timeSave" :productEdit="productSelected" ></product-save>
        </div>
     `      
});
