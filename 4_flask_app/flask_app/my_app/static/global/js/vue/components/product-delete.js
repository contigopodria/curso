Vue.component('product-delete', {
    props: ['product','time'],
    data: function () {
        return {
            products: [] 
        }
    },
    
    methods: {
        productDelete: function () {
            /* Creamos fetch que es una promesa*/
            fetch('http://localhost:5000/api/products/'+this.product.id,{method: 'DELETE'})
                .then(res => res.json())
                .then(res => this.$emit('eventProductDelete'))
        }
    },
    watch: {
        time: function (newValue, oldValue) {
            $('#deleteModal').modal('show')
        }
    },
     template:
     `
        <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel"
            aria-hidden="true">
            <div class="modal-dialog">
                <div v-if="product" class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title" id="deleteModalLabel">Borrar: {{ product.name }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body bg-light text-danger">
                        ¡ ATENCION !
                        <br>
                        Ésta acción eliminará totalmente el producto
                    </div>
                    <div class="modal-footer">
                        <button @click="productDelete" class="btn btn-outline-danger btn-sm" data-bs-dismiss="modal"><i class="fa fa-eraser"></i>Eliminar</button>
                        <button type="button" class="btn btn-outline-secondary btn-sm" data-bs-dismiss="modal"><i class="fa fa-arrow-right-from-bracket"></i>Cerrar</button>
                        </div>
                    </div>
                </div>    
            </div>
        </div>
     `      
});
