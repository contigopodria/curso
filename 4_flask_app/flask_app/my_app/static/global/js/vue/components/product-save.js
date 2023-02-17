Vue.component('product-save', {
    props: {
        time: Number,
        productEdit: {
            type: Object,
            default: undefined
        }

    },
    data: function () {
        return {
            products: [],
            fname: '',
            fprice: 0,
            fcategory_id:0,
            product: '',
            error: '',
            categories: [] 
        }
    },
    created(){
        this.getCategories()
    },
    methods: {
        getCategories: function () {
            fetch('http://localhost:5000/api/categories/')
                .then(res => res.json())
                .then(res => {
                    if (res.code == 200) {
                        this.categories = res.data
                    }
                    else {
                        this.error = res.msj
                    }
                })  
        },
        productSave: function () {
            var formData = new FormData()
            formData.append('name', this.fname)
            formData.append('price', this.fprice)
            formData.append('category_id', this.fcategory_id)
            this.error = ""
            if (this.productEdit) {
                this.productUpdate(formData)
            }
            else {
                this.productInsert(formData)
            }
        },
        productInsert: function(formData) {
            fetch('http://localhost:5000/api/products/',{ 
                method: 'POST', 
                body: formData
                })
                .then(res => res.json())
                .then(res => {
                    if (res.code == 200) {
                        this.product = res
                        this.$emit('eventProductInsert', this.product)
                        $('#saveModal').modal('hide')
                    }
                    else {
                        this.error = res.msj
                    }
                })
        },
        productUpdate: function (formData) {
            fetch('http://localhost:5000/api/products/'+ this.productEdit.id, {
                method: 'PUT',
                body: formData
                })
                .then(res => res.json())
                .then(res => {
                    if (res.code == 200) {
                        this.product = res
                        this.$emit('eventProductUpdate', this.product)
                        $('#saveModal').modal('hide')
                    }
                    else {
                        this.error = res.msj
                    }
                })
        }
    },
    watch: {
        time: function (newValue, oldValue) {
            this.error = ""
            $('#saveModal').modal('show')
            if (this.productEdit) {
                this.fname = this.productEdit.name
                this.fprice = this.productEdit.price
                this.fcategory_id = this.productEdit.category_id
            }
            else {
                this.fname = ''
                this.fprice = 0
                this.fcategory_id = 0
            }
        }
    },
     template:
     `
        <div class="modal fade" id="saveModal" tabindex="-1" aria-labelledby="saveModalLabel"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title" id="saveModalLabel">Crear producto</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body bg-light text-danger"> 
                        <div v-if="error" class = "alert alert-danger">
                        {{ error }}
                        </div>
                        <div class="form-group mb-3 mt-3">
                            <label for="name">Nombre</label>
                            <input class="form-control mt-1" v-model="fname" type="text" value="">
                        </div>
                        <div class="form-group">
                            <label for="price">Precio</label>
                            <input class="form-control mt-1" v-model="fprice" type="number" value="">
                        </div>
                        <div class="form-group">
                            <label for="category_id">Categoria</label>
                            <select class="form-select mt-1" v-model="fcategory_id">
                                <option v-for="c in categories" :value="c.id">{{ c.name }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button @click="productSave" class="btn btn-outline-success btn-sm"><i class="fa fa-check-double"></i>Aceptar</button>
                        <button type="button" class="btn btn-outline-secondary btn-sm" data-bs-dismiss="modal"><i class="fa fa-arrow-right-from-bracket"></i>Cerrar</button>
                        </div>
                    </div>
                </div>    
            </div>
        </div>
     `      
});
