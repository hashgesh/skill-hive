---
name: refactor
description: Analyze code for refactoring opportunities, apply refactoring patterns, and automate improvements using AST tools. Based on refactoring.guru catalog.
---

# Refactor Skill

Guidelines for analyzing code, identifying refactoring opportunities, and applying refactoring patterns. Based on the [refactoring.guru](https://refactoring.guru/refactoring/catalog) catalog.

## Install

```bash
# ast-grep for automated refactoring
cargo install ast-grep

# or via npm
npm install -g ast-grep
```

## Code Smells (Analysis)

Source: [refactoring.guru/refactoring/smells](https://refactoring.guru/refactoring/smells)

### 1. Bloaters

Methods and classes that have increased to gargantuan proportions.

| Smell | Signs | Fix |
|-------|-------|-----|
| **Long Method** | >10 lines, hard to understand | Extract Method |
| **Large Class** | >500 lines, too many fields | Extract Class |
| **Primitive Obsession** | Overuse of primitives for domain types | Replace Primitive with Object |
| **Long Parameter List** | >4 parameters | Introduce Parameter Object |
| **Data Clumps** | Same fields in multiple classes | Extract Class |

### 2. Object-Orientation Abusers

Incomplete or incorrect OOP application.

| Smell | Signs | Fix |
|-------|-------|-----|
| **Switch Statements** | Repeated switch/case | Replace with Polymorphism |
| **Temporary Field** | Fields set only in certain conditions | Extract Class |
| **Refused Bequest** | Subclass uses little of parent | Push Down Method |
| **Alternative Classes** | Same interface, different implementations | Extract Interface |

### 3. Change Preventers

One change requires many other changes.

| Smell | Signs | Fix |
|-------|-------|-----|
| **Divergent Change** | One class changed in many ways | Extract Class |
| **Shotgun Surgery** | One change requires changes in many classes | Move Method |
| **Parallel Inheritance** | Two hierarchies mirroring each other | Combine into one |

### 4. Dispensables

Pointless, unneeded code that makes things messy.

| Smell | Signs | Fix |
|-------|-------|-----|
| **Comments** | Explaining bad code | Extract Method, Rename |
| **Duplicate Code** | Identical in 2+ places | Extract Method |
| **Lazy Class** | Does too little | Inline Class |
| **Data Class** | Only data, no behavior | Move Method |
| **Dead Code** | Unused code | Delete |
| **Speculative Generality** | "Just in case" code | Inline Class |

### 5. Couplers

Excessive coupling between classes.

| Smell | Signs | Fix |
|-------|-------|-----|
| **Feature Envy** | Method uses more of another class | Move Method |
| **Inappropriate Intimacy** | Class knows too much about another | Move Method, Change Bidirectional to Unidirectional |
| **Message Chains** | A -> B -> C calls | Hide Delegate |
| **Middle Man** | Class only delegates | Remove Middle Man |

---

## Refactoring Techniques

Source: [refactoring.guru/refactoring/techniques](https://refactoring.guru/refactoring/techniques)

### 1. Composing Methods

| Pattern | When to Use | Eliminates |
|---------|-------------|------------|
| **Extract Method** | Code can be grouped together | Long Method, Duplicate Code |
| **Inline Method** | Method body clearer than name | - |
| **Extract Variable** | Complex expression | - |
| **Inline Temp** | Temp used once | - |
| **Replace Temp with Query** | Temp holding expression result | Long Parameter List |
| **Split Temporary Variable** | Multiple assignments to temp | - |
| **Remove Assignments to Parameters** | Assigning to params | - |

### 2. Moving Features Between Objects

| Pattern | When to Use |
|---------|-------------|
| **Move Method** | Method uses more of another class |
| **Move Field** | Field used more by another class |
| **Extract Class** | One class doing two things |
| **Inline Class** | Class doing too little |
| **Hide Delegate** | Client calling delegate |
| **Remove Middle Man** | Too much delegation |
| **Introduce Foreign Method** | Library class needs modification |
| **Introduce Local Extension** | Need extra methods on library class |

### 3. Organizing Data

| Pattern | When to Use |
|---------|-------------|
| **Self Encapsulate Field** | Need flexible field access |
| **Replace Data Value with Object** | Primitive for domain concept |
| **Change Value to Reference** | Multiple copies of same object |
| **Change Reference to Value** | Object rarely modified |
| **Replace Array with Object** | Array with named elements |
| **Duplicate Observed Data** | GUI and domain coupled |
| **Change Unidirectional to Bidirectional** | Need reverse reference |
| **Change Bidirectional to Unidirectional** | Unnecessary coupling |
| **Replace Magic Number with Constant** | Magic numbers in code |
| **Encapsulate Field** | Public field |
| **Encapsulate Collection** | Returning raw collection |
| **Replace Type Code with Class** | Type code as data |
| **Replace Type Code with Subclasses** | Type affects behavior |
| **Replace Type Code with State/Strategy** | State transitions |
| **Replace Subclass with Fields** | Simple subclass differences |

### 4. Simplifying Conditional Expressions

| Pattern | When to Use |
|---------|-------------|
| **Decompose Conditional** | Complex if/else |
| **Consolidate Conditional Expression** | Multiple checks → same result |
| **Consolidate Duplicate Fragments** | Same code in all branches |
| **Remove Control Flag** | Boolean flag for loop |
| **Replace Nested Conditionals with Guard Clauses** | Arrow pattern |
| **Replace Conditional with Polymorphism** | Type affects behavior |
| **Introduce Null Object** | Repeated null checks |
| **Introduce Assertion** | Code assumes something |

### 5. Simplifying Method Calls

| Pattern | When to Use |
|---------|-------------|
| **Rename Method** | Name doesn't reveal intent |
| **Add Parameter** | Need more data |
| **Remove Parameter** | Unused parameter |
| **Separate Query from Modifier** | Method both queries and modifies |
| **Parameterize Method** | Similar methods with different values |
| **Replace Parameter with Explicit Methods** | Different param → different behavior |
| **Preserve Whole Object** | Getting several values from object |
| **Replace Parameter with Method Call** | Parameter derived from other params |
| **Introduce Parameter Object** | Parameters belong together |
| **Remove Setting Method** | Field should never change |
| **Hide Method** | Not used by other classes |
| **Replace Constructor with Factory** | Need special construction |
| **Replace Error Code with Exception** | Error handling via return codes |
| **Replace Exception with Test** | Exception used for control flow |

### 6. Dealing with Generalization

| Pattern | When to Use |
|---------|-------------|
| **Pull Up Field** | Field used by all subclasses |
| **Pull Up Method** | Method identical in subclasses |
| **Pull Up Constructor Body** | Common constructor code |
| **Push Down Method** | Method used by one subclass only |
| **Push Down Field** | Field used by one subclass only |
| **Extract Subclass** | Class has features used only in some cases |
| **Extract Superclass** | Similar classes |
| **Extract Interface** | Need consistent interface |
| **Collapse Hierarchy** | Superclass and subclass too similar |
| **Form Template Method** | Same steps, different implementations |
| **Replace Inheritance with Delegation** | Inheritance misused |
| **Replace Delegation with Inheritance** | Too much delegation |

---

## Extract Method (Example)

Source: [refactoring.guru/extract-method](https://refactoring.guru/extract-method)

### Problem
Code fragment can be grouped together.

### Solution
Move to separate method, replace old code with call.

### Before
```java
void printOwing() {
  printBanner();
  System.out.println("name: " + name);
  System.out.println("amount: " + getOutstanding());
}
```

### After
```java
void printOwing() {
  printBanner();
  printDetails(getOutstanding());
}

void printDetails(double outstanding) {
  System.out.println("name: " + name);
  System.out.println("amount: " + outstanding);
}
```

### Steps
1. Create new method with self-evident name
2. Copy code to new method, replace old with call
3. Pass variables as parameters
4. Return modified values if needed

---

## Automated Refactoring (ast-grep)

Use ast-grep for safe, automated refactoring:

```bash
# Find all console.log
sg query -p console.log -l

# Replace with logger
sg -r 'logger.info($MSG)' -p 'console.log($MSG)'

# Find todo comments
sg -p '// TODO' -l

# Find magic numbers
sg -p '100' --lang rust

# Find long functions (>20 lines)
sg query -l -p 'function $NAME($$$) { $$$ }' --json | jq '.[] | select(.node.text | length > 500)'
```

---

## Decision Guide

**When to refactor:**
- Before adding features
- When fixing bugs
- During code review
- When understanding code

**When NOT to refactor:**
- Code about to be replaced
- Tight deadline
- No tests (write tests first)
- External interface (breaking change)

**Safety First:**
1. Run tests before and after
2. Commit before refactoring
3. Small, incremental changes
4. Use automated tools (ast-grep)

---

## Workflow

1. **Analyze** - Identify smell, check complexity
2. **Plan** - Choose pattern, list affected files
3. **Execute** - Small changes, run tests, commit
4. **Verify** - Tests pass, code clearer, no new smells

---

## Rules

1. One refactoring at a time
2. Never change behavior (tests must pass)
3. Commit after each step
4. Rename is most valuable refactoring
5. Extract first, then inline if needed

---

## Examples

### Replace Nested Conditionals with Guard Clauses
```javascript
// Before
function getPaymentType(order) {
  if (order) {
    if (order.customer) {
      if (order.customer.premium) {
        return 'premium';
      }
      return 'regular';
    }
    return 'guest';
  }
  return 'none';
}

// After
function getPaymentType(order) {
  if (!order) return 'none';
  if (!order.customer) return 'guest';
  return order.customer.premium ? 'premium' : 'regular';
}
```

### Introduce Null Object
```javascript
// Before
function getShippingAddress(user) {
  if (user === null) return "Unknown";
  if (user.address === null) return "No address";
  return user.address;
}

// After
const NullUser = {
  address: "Unknown",
  getShippingAddress() { return this.address; }
};

function getShippingAddress(user) {
  const u = user || NullUser;
  return u.address || "No address";
}
```

---

## Validation Checklist

- [ ] All tests pass
- [ ] Code is shorter/clearer
- [ ] No new code smells introduced
- [ ] Intent is clearer
- [ ] No duplicate code created
- [ ] Names are descriptive
