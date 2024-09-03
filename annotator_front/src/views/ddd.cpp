#include <stdio.h>
#define HASH_SIZE 18
#define NUM_KEYS 11

// 哈希表和比较次数数组
int hashTable[HASH_SIZE];
int comparisons[HASH_SIZE];

// 初始化哈希表和比较次数数组
void initializeHashTable() {
    for (int i = 0; i < HASH_SIZE; i++) {
        hashTable[i] = -1;  // 使用-1表示空槽位
        comparisons[i] = 0;
    }
}

// 插入函数，使用线性探测法
void hashInsert(int numbers[], int n) {
    for (int i = 0; i < n; i++) {
        int num = numbers[i];
        int index = num % HASH_SIZE;

        while (hashTable[index] != -1) {
            index = (index + 1) % HASH_SIZE;
        }

        hashTable[index] = num;
    }
}

// 查找函数，返回查找次数
int hashSearch(int key) {
    int index = key % HASH_SIZE;
    int start = index;
    int count = 0;

    do {
        count++;
        if (hashTable[index] == key) {
            printf("Key %d found at address %d with %d comparisons.\n", key, index, count);
            return index;
        }
        index = (index + 1) % HASH_SIZE;
    } while (index != start);

    printf("Key %d not found after %d comparisons.\n", key, count);
    return -1;
}

int main() {
    int numbers[NUM_KEYS];
    int keyToFind;

    printf("Enter 11 numbers separated by spaces: ");
    for (int i = 0; i < NUM_KEYS; i++) {
        scanf("%d", &numbers[i]);
    }

    initializeHashTable();
    hashInsert(numbers, NUM_KEYS);

    printf("Enter the key to find: ");
    scanf("%d", &keyToFind);

    hashSearch(keyToFind);

    return 0;
}
