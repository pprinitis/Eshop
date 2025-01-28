<template>
    <td v-if="!hideId"> {{ item.id }}</td>

    <td>{{ item.title }}</td>

    <td>
        <img :src="item.img" alt="Product Image" class="table-image" />
    </td>

    <td>{{ item.price }} €</td>

    <td v-if="!hideQuantity"> {{ item.quantity }}</td>

</template>

<script setup>
defineProps({
    item: {
        type: Object,
        required: true,
    },
    hideId: {
        type: Boolean,
        default: false,
    },
    hideQuantity: {
        type: Boolean,
        default: false,
    }
});
</script>